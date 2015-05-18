from collections import namedtuple
from datetime import datetime


DemirBankResponse = namedtuple('DemirBankResponse', 'AuthCode EXTRA_CARDBRAND EXTRA_TRXDATE ErrMsg HASH '
                                                    'HASHPARAMS HASHPARAMSVAL HostRefNum MaskedPan PAResSyntaxOK '
                                                    'PAResVerified ProcReturnCode Response ReturnOid '
                                                    'TransId amount cavv clientid currency eci md rnd mdErrorMsg '
                                                    'mdStatus merchantID oid storetype txstatus clientIp')


class DemirBankSuccessResponseParser(object):
    def parse_response(self, payment_details):
        response = DemirBankResponse(
            AuthCode=payment_details.get('AuthCode'),
            EXTRA_CARDBRAND=payment_details.get('EXTRA.CARDBRAND'),
            EXTRA_TRXDATE=datetime.strptime(payment_details.get('EXTRA.TRXDATE'), "%Y%m%d %H:%M:%S"),
            ErrMsg=payment_details.get('ErrMsg'),
            HASH=payment_details.get('HASH'),
            HASHPARAMS=payment_details.get('HASHPARAMS'),
            HASHPARAMSVAL=payment_details.get('HASHPARAMSVAL'),
            HostRefNum=payment_details.get('HostRefNum'),
            MaskedPan=payment_details.get('MaskedPan'),
            PAResSyntaxOK=bool(payment_details.get('PAResSyntaxOK')),
            PAResVerified=bool(payment_details.get('PAResVerified')),
            ProcReturnCode=payment_details.get('ProcReturnCode'),
            Response=payment_details.get('Response'),
            ReturnOid=payment_details.get('ReturnOid'),
            TransId=payment_details.get('TransId'),
            amount=int(payment_details.get('amount')),
            cavv=payment_details.get('cavv'),
            clientid=payment_details.get('clientid'),
            currency=int(payment_details.get('currency')),
            eci=payment_details.get('eci'),
            md=payment_details.get('md'),
            rnd=payment_details.get('rnd'),
            mdErrorMsg=payment_details.get('mdErrorMsg'),
            mdStatus=int(payment_details.get('mdStatus')),
            merchantID=payment_details.get('merchantID'),
            oid=payment_details.get('oid'),
            storetype=payment_details.get('storetype'),
            txstatus=payment_details.get('txstatus'),
            clientIp=payment_details.get('clientIp'),
        )
        return response


class DemirBankFailResponseParser(object):
    def parse_response(self, payment_details):
        response = DemirBankResponse(
            AuthCode='',
            EXTRA_CARDBRAND='',
            EXTRA_TRXDATE=None,
            ErrMsg=payment_details.get('ErrMsg', ''),
            HASH=payment_details.get('HASH'),
            HASHPARAMS=payment_details.get('HASHPARAMS'),
            HASHPARAMSVAL=payment_details.get('HASHPARAMSVAL'),
            Response=payment_details.get('Response', ''),
            amount=int(payment_details.get('amount')),
            clientid=payment_details.get('clientid'),
            clientIp=payment_details.get('clientIp'),
            currency=int(payment_details.get('currency')),
            mdErrorMsg=payment_details.get('mdErrorMsg'),
            mdStatus=int(payment_details.get('mdStatus')),
            oid=payment_details.get('oid'),

            ProcReturnCode=payment_details.get('ProcReturnCode', ''),
            rnd=payment_details.get('rnd', ''),
            PAResSyntaxOK=bool(payment_details.get('PAResSyntaxOK', 'false')),
            ReturnOid=payment_details.get('ReturnOid', ''),
            PAResVerified=bool(payment_details.get('PAResVerified', 'false')),
            TransId='',
            cavv=payment_details.get('cavv', ''),
            eci=payment_details.get('eci', ''),
            md=payment_details.get('md', ''),
            merchantID=payment_details.get('merchantID', ''),
            storetype=payment_details.get('storetype', ''),
            txstatus=payment_details.get('txstatus', ''),
            HostRefNum='',
            MaskedPan=payment_details.get('MaskedPan', '')
        )
        return response