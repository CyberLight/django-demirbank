# django-demirbank
Django library for demirbank payments

# Simple usage of library


### For example, put this keys inside settings.py
```
DEMIR_BANK_PAY_ACTION_URL = 'https://to.processing.site/fim'
DEMIR_BANK_CLIENT_ID = 'XXXXXXXXXXX'
DEMIR_BANK_TRANSACTION_TYPE = 'Auth'
DEMIR_BANK_INSTALMENT = ''
DEMIR_BANK_OK_URL = 'http://to.yout.site/path/to/pay/success'
DEMIR_BANK_FAIL_URL = 'http://to.yout.site/path/to/pay/fail'
DEMIR_BANK_STORE_TYPE = '3d_Pay_Hosting'
DEMIR_BANK_LANG = 'ru'
DEMIR_BANK_CURRENCY_CODE = 417 # som
DEMIR_BANK_STORE_KEY = 'STORE_KEY_RECEIVED_FROM_BANK'

DEMIR_BANK_CLIENT_MODEL_PATH = 'app.models'
DEMIR_BANK_CLIENT_MODEL_NAME = 'Client'
DEMIR_BANK_CLIENT_MODEL_SEARCH_FIELD = 'phone_number'
DEMIR_BANK_CLIENT_MODEL_UPDATE_BALANCE_METHOD_NAME = 'update_balance_demirbank'
```

### For example, put this code inside view.py 

```Python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
from django.views.generic import View

from demirbank.views import PaymentMixin

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Client
CLIENT_ACCOUNT = '0555123123'


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class PayFormView(View, PaymentMixin):

    def get(self, request, *args, **kwargs):
        Client.objects.get_or_create(phone_number=CLIENT_ACCOUNT)
        payment_form_data = self.generate_payment(account=CLIENT_ACCOUNT,
                                                  amount=request.GET.get('amount', 0),
                                                  currency=settings.DEMIR_BANK_CURRENCY_CODE)
        return render(request, 'pay.html', payment_form_data)


class PayFailView(PaymentMixin, CSRFExemptMixin, View):

    def post(self, request, *args, **kwargs):

        self.fail_payment(request.POST.dict())
        return self.DemirBankHttpResponse()



class PaySuccessView(PaymentMixin, CSRFExemptMixin, View):

    def post(self, request, *args, **kwargs):
        self.success_payment(request.POST.dict(), "Пополнение баланса")
        return self.DemirBankHttpResponse()

```

### For model Client
  * Need to add method ```update_balance_demirbank``` to Client model with following arguments
```
def update_balance_demirbank(self, money, reason, **kwargs):
    pass
```
