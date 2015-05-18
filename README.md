# django-demirbank
Django library for demirbank payments

# Simple usage of library


### For example, put this keys inside settings.py
```
PAY_ACTION_URL = 'https://to.processing.site/fim'
CLIENT_ID = 'XXXXXXXXXXX'
TRANSACTION_TYPE = 'Auth'
INSTALMENT = ''
OK_URL = 'http://to.yout.site/path/to/pay/success'
FAIL_URL = 'http://to.yout.site/path/to/pay/fail'
STORE_TYPE = '3d_Pay_Hosting'
LANG = 'ru'
CURRENCY_CODE = 417
STORE_KEY = 'STORE_KEY_RECEIVED_FROM_BANK'

DEMIR_BANK_CLIENT_MODEL_PATH = 'app.models'
DEMIR_BANK_CLIENT_MODEL_NAME = 'Client'
DEMIR_BANK_CLIENT_MODEL_SEARCH_FIELD = 'phone_number'
DEMIR_BANK_CLIENT_MODEL_UPDATE_BALANCE_METHOD_NAME = 'update_balance_demirbank'
```

### For example, put this code inside view.py 

```Python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
from demirbank.views import PaymentMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from time import time
from .models import Client
CLIENT_ACCOUNT = 'XXXXXXXXXX'


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class PayFormView(View, PaymentMixin):

    def get(self, request, *args, **kwargs):
        Client.objects.get_or_create(phone_number=CLIENT_ACCOUNT)
        payment_form_data = self.generate_payment(order_id=int(time()),
                                                  account=CLIENT_ACCOUNT,
                                                  amount=request.GET.get('amount', 0),
                                                  currency=settings.CURRENCY_CODE)
        return render(request, 'pay.html', payment_form_data)


class PayFailView(PaymentMixin, CSRFExemptMixin, View):

    def post(self, request, *args, **kwargs):
        self.fail_payment(CLIENT_ACCOUNT, request.POST.dict())
        return HttpResponse('0', 'text/plain')

    def get(self, request, *args, **kwargs):
        return render(request, 'pay_fail.html', {})


class PaySuccessView(PaymentMixin, CSRFExemptMixin, View):

    def post(self, request, *args, **kwargs):
        self.success_payment(CLIENT_ACCOUNT, request.POST.dict())
        return HttpResponse('0', 'text/plain')

    def get(self, request, *args, **kwargs):
        return render(request, 'pay_success.html', {})
```
