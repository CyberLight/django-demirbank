from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
import base64
from hashlib import sha1
import binascii
from utils import microtime
from collections import namedtuple
import messages
import_client_model = "from {0} import {1} as Client".format(settings.DEMIR_BANK_CLIENT_MODEL_PATH,
                                                             settings.DEMIR_BANK_CLIENT_MODEL_NAME)
exec import_client_model

PayForm = namedtuple('PayForm', 'pay_action_url client_id amount transaction_type '
                                'instalment oid ok_url fail_url rnd store_type lang '
                                'currency hash')


class DemirBankException(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RequestVerificationFailedException(DemirBankException):
    pass


class AccountDoesNotExistException(DemirBankException):
    pass


class InvalidAmountValueException(DemirBankException):
    pass


class InvalidOrderIdValueException(DemirBankException):
    pass


class PaymentMixin(object):

    DEMIR_BANK_HASH_KEY = 'HASH'
    DEMIR_BANK_HASHPARAMSVAL = 'HASHPARAMSVAL'
    DEMIR_BANK_HASHPARAMS = 'HASHPARAMS'

    def generate_payment(self, order_id, account, amount):
        if not self._account_exists(account):
            raise AccountDoesNotExistException()

        if not self._valid_amount(amount):
            raise InvalidAmountValueException()

        if not self._valid_order_id(order_id):
            raise InvalidOrderIdValueException()

        pay_form = PayForm(pay_action_url=settings.PAY_ACTION_URL,
                           client_id=settings.CLIENT_ID,
                           amount=amount,
                           transaction_type=settings.TRANSACTION_TYPE,
                           instalment='',
                           oid=order_id,
                           ok_url=settings.OK_URL,
                           fail_url=settings.FAIL_URL,
                           rnd=microtime(),
                           store_type=settings.STORE_TYPE,
                           lang=settings.LANG,
                           currency=settings.CURRENCY_CODE)

        pay_form.hash = self._generate_hash(str(pay_form.client_id) +
                                            str(pay_form.oid) +
                                            str(pay_form.amount) +
                                            str(pay_form.ok_url) +
                                            str(pay_form.fail_url) +
                                            str(pay_form.transaction_type) +
                                            str(pay_form.instalment) +
                                            str(pay_form.rnd) +
                                            str(settings.STORE_KEY))

        return pay_form

    def success_payment(self, account, payment_details):
        if not self._account_exists(account):
            raise AccountDoesNotExistException()

        if not self._valid_order_id(payment_details.get('oid', '')):
            raise InvalidOrderIdValueException()

    def fail_payment(self, account, payment_details):
        pass

    def _check_payment_sign(self, payment_details):
        bank_hash = payment_details.get(self.DEMIR_BANK_HASH_KEY, '')
        bank_hash_value = payment_details.get(self.DEMIR_BANK_HASHPARAMSVAL, '')
        bank_hash_params = payment_details.get(self.DEMIR_BANK_HASHPARAMS, '')
        params_keys = filter(None, bank_hash_params.split(':'))

        hash_values = ''
        for key in params_keys:
            hash_values += payment_details.get(key, '')

        if not hash_values or not bank_hash_value:
            raise RequestVerificationFailedException(value=messages.MESSAGE_EMPTY_HASHPARAMSVAL)

        if hash_values != bank_hash_value:
            raise RequestVerificationFailedException(value=messages.HASH_VALUES_DO_NOT_MATCH)

        store_key = settings.STORE_KEY
        hash_values += store_key
        calculated_hash = self._generate_hash(hash_values)
        if not calculated_hash == bank_hash:
            raise RequestVerificationFailedException(value=messages.HASHES_DO_NOT_MATCHED)

    def _generate_hash(self, hash_values):
        return base64.b64encode(binascii.unhexlify(sha1(hash_values).hexdigest()))

    def _account_exists(self, account):
        pass

    def _valid_amount(self, amount):
        pass

    def _valid_order_id(self, order_id):
        return not order_id
