# -*- coding: utf-8 -*-

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


class PaymentAlreadyProcessedOrNotExistsException(DemirBankException):
    pass


class InvalidCurrencyCodeException(DemirBankException):
    pass
