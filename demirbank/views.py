# -*- coding: utf-8 -*-

from django.conf import settings
import base64
from hashlib import sha1
import binascii
from django.http import HttpResponse
from utils import microtime
from collections import namedtuple, OrderedDict
import messages
from models import DemirBankPayment
from parsers import DemirBankSuccessResponseParser, DemirBankFailResponseParser
import re
import uuid
from errors import RequestVerificationFailedException, AccountDoesNotExistException, \
    InvalidAmountValueException, InvalidOrderIdValueException, PaymentAlreadyProcessedOrNotExistsException, \
    InvalidCurrencyCodeException

app = __import__(settings.DEMIR_BANK_CLIENT_MODEL_PATH, fromlist=[settings.DEMIR_BANK_CLIENT_MODEL_NAME])
Client = getattr(app, settings.DEMIR_BANK_CLIENT_MODEL_NAME)

CLIENT_SEARCH_FIELD = settings.DEMIR_BANK_CLIENT_MODEL_SEARCH_FIELD

PayForm = namedtuple('PayForm', 'pay_action_url client_id amount transaction_type '
                                'instalment oid ok_url fail_url rnd store_type lang '
                                'currency hash')

class PaymentMixin(object):
    DEMIR_BANK_HASH_KEY = 'HASH'
    DEMIR_BANK_HASHPARAMSVAL = 'HASHPARAMSVAL'
    DEMIR_BANK_HASHPARAMS = 'HASHPARAMS'

    def __init__(self):
        self.client = None
        self.payment = None

    def generate_payment(self, account, amount, currency, order_id=''):

        if not self._account_exists(account):
            raise AccountDoesNotExistException(value=account)

        if not self._valid_amount(amount):
            raise InvalidAmountValueException(value=messages.INVALID_AMOUNT_VALUE)

        if not order_id:
            order_id = str(uuid.uuid4()).replace('-', '')

        if not self._valid_order_id(order_id):
            raise InvalidOrderIdValueException(value=messages.INVALID_ORDER_ID)

        if not self._valid_currency(currency):
            raise InvalidCurrencyCodeException(value=messages.INVALID_CURRENCY_CODE)

        self._create_new_payment(account=account,
                                 amount=amount,
                                 order_id=order_id,
                                 currency=currency)

        pay_form = self._generate_pay_form(amount=amount,
                                           currency=currency,
                                           order_id=order_id)

        return pay_form

    def success_payment(self, payment_details, payment_reason):
        return self._process_response(payment_details, DemirBankSuccessResponseParser, payment_reason)

    def fail_payment(self, payment_details):
        return self._process_response(payment_details, DemirBankFailResponseParser)

    def _check_payment_sign(self, payment_details):
        bank_hash = payment_details.get(self.DEMIR_BANK_HASH_KEY, '')
        bank_hash_value = payment_details.get(self.DEMIR_BANK_HASHPARAMSVAL, '')
        bank_hash_params = payment_details.get(self.DEMIR_BANK_HASHPARAMS, '')
        params_keys = filter(None, bank_hash_params.split(':'))

        hash_values = ''
        for key in params_keys:
            hash_values += str(payment_details.get(self._normalize_key(key), 'null'))

        if not hash_values or not bank_hash_value:
            raise RequestVerificationFailedException(value=messages.MESSAGE_EMPTY_HASHPARAMSVAL)

        if hash_values != bank_hash_value:
            raise RequestVerificationFailedException(value=messages.HASH_VALUES_DO_NOT_MATCH)

        store_key = settings.DEMIR_BANK_STORE_KEY
        hash_values += store_key
        calculated_hash = self._generate_hash(hash_values)
        if not calculated_hash == bank_hash:
            raise RequestVerificationFailedException(value=messages.HASHES_DO_NOT_MATCHED)

    def _normalize_key(self, key_name):
        key_mapping = {
            'ClientId': 'clientid',
            'OrderId': 'oid'
        }
        new_key_value = key_mapping.get(key_name, None)
        return key_name if not new_key_value else new_key_value

    def _generate_pay_form(self, amount, currency, order_id):
        pay_form = PayForm(pay_action_url=settings.DEMIR_BANK_PAY_ACTION_URL,
                           client_id=settings.DEMIR_BANK_CLIENT_ID,
                           amount=int(amount),
                           transaction_type=settings.DEMIR_BANK_TRANSACTION_TYPE,
                           instalment=settings.DEMIR_BANK_INSTALMENT,
                           oid=order_id,
                           ok_url=settings.DEMIR_BANK_OK_URL,
                           fail_url=settings.DEMIR_BANK_FAIL_URL,
                           rnd=microtime(),
                           store_type=settings.DEMIR_BANK_STORE_TYPE,
                           lang=settings.DEMIR_BANK_LANG,
                           currency=currency,
                           hash='')
        pay_form = pay_form._replace(hash=self._generate_hash(str(pay_form.client_id) +
                                                              str(pay_form.oid) +
                                                              str(pay_form.amount) +
                                                              str(pay_form.ok_url) +
                                                              str(pay_form.fail_url) +
                                                              str(pay_form.transaction_type) +
                                                              str(pay_form.instalment) +
                                                              str(pay_form.rnd) +
                                                              str(settings.DEMIR_BANK_STORE_KEY)))
        return OrderedDict(zip(pay_form._fields, pay_form))

    def _create_new_payment(self, account, amount, order_id, currency):
        payment = DemirBankPayment()
        payment.oid = order_id
        payment.amount = int(amount)
        payment.account = account
        payment.currency = currency
        payment.save()

    def _process_response(self, payment_details, parser_class, payment_reason=''):

        order_id = payment_details.get('oid', '')
        if not self._valid_order_id(order_id):
            raise InvalidOrderIdValueException()

        if self._payment_exists(order_id):

            account = self.payment.account
            if not self._account_exists(account):
                raise AccountDoesNotExistException(value=account)

            parser = parser_class()
            parsed_response = parser.parse_response(payment_details)
            parsed_response_dict = OrderedDict(zip(parsed_response._fields, parsed_response))
            self._check_payment_sign(parsed_response_dict)
            self._fill_payment_with(parsed_response)
            self.payment.save()

            if self.payment.added:
                update_balance_demirbank = getattr(self.client,
                                                   settings.DEMIR_BANK_CLIENT_MODEL_UPDATE_BALANCE_METHOD_NAME)
                update_balance_demirbank(self.payment.amount, payment_reason, payment=self.payment)
            return self.payment

        raise PaymentAlreadyProcessedOrNotExistsException(value=messages.PAYMENT_ALREADY_PROCESSED_OR_NOT_EXISTS)

    def _generate_hash(self, hash_values):
        return base64.b64encode(binascii.unhexlify(sha1(hash_values).hexdigest()))

    def _account_exists(self, account):
        try:
            search_condition = {CLIENT_SEARCH_FIELD: account}
            self.client = Client.objects.get(**search_condition)
            return True
        except Client.DoesNotExist:
            return False

    def _valid_amount(self, amount):
        try:
            return int(amount) > 0
        except ValueError:
            return False

    def _valid_currency(self, currency):
        try:
            int(currency)
            return True
        except ValueError:
            return False

    def _valid_order_id(self, order_id):
        return order_id and re.match('^[a-zA-Z0-9]+$', order_id)

    def _payment_exists(self, order_id):
        try:
            self.payment = DemirBankPayment.objects.get(oid=order_id,
                                                        added=False,
                                                        processed_payment=False)
            return True
        except DemirBankPayment.DoesNotExist:
            return False

    def _fill_payment_with(self, parsed):
        self.payment.auth_code = parsed.AuthCode
        self.payment.extra_cardbrand = parsed.EXTRA_CARDBRAND
        self.payment.extra_trxdate = parsed.EXTRA_TRXDATE
        self.payment.err_msg = parsed.ErrMsg
        self.payment.hash = parsed.HASH
        self.payment.hash_params = parsed.HASHPARAMS
        self.payment.hash_params_val = parsed.HASHPARAMSVAL
        self.payment.host_ref_num = parsed.HostRefNum
        self.payment.masked_pan = parsed.MaskedPan
        self.payment.pa_res_syntax_ok = parsed.PAResSyntaxOK
        self.payment.pa_res_verified = parsed.PAResVerified
        self.payment.proc_return_code = parsed.ProcReturnCode
        self.payment.response = parsed.Response
        self.payment.return_oid = parsed.ReturnOid
        self.payment.trans_id = parsed.TransId
        self.payment.cavv = parsed.cavv
        self.payment.client_id = parsed.clientid
        self.payment.eci = parsed.eci
        self.payment.md = parsed.md
        self.payment.rnd = parsed.rnd
        self.payment.md_error_msg = parsed.mdErrorMsg
        self.payment.md_status = parsed.mdStatus
        self.payment.merchant_id = parsed.merchantID
        self.payment.oid = parsed.oid
        self.payment.storetype = parsed.storetype
        self.payment.txstatus = parsed.txstatus
        self.payment.client_ip = parsed.clientIp
        self.payment.added = (parsed.Response == 'Approved' and
                              parsed.mdStatus == 1 and
                              parsed.ProcReturnCode == '00')
        self.payment.processed_payment = True

    def DemirBankHttpResponse(self):
        return HttpResponse('0', 'text/plain')
