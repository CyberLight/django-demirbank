Library django-demirbank
=======================

* Supports only one operation "Selling" (type **Auth**) which includes **Pre-Auth** and **Post-Auth**
* Supported only following settings
  * ```STORE_TYPE = '3d_Pay_Hosting'```
  * ```TRANSACTION_TYPE = 'Auth'```

* Library settings:
  * The following settings needs to add inside "settings/dev.py"
    * PAY_ACTION_URL = 'url/to/demirbank/proces'
    * CLIENT_ID = 12345678 # client id
    * TRANSACTION_TYPE = 'Auth' # type for Selling operation
    * INSTALMENT = '' # empty string for this parameter
    * OK_URL = 'url/to/merchant/success/page'
    * FAIL_URL = 'url/to/merchant/error/page'
    * STORE_TYPE = '3d_Pay_Hosting'
    * LANG = 'ru' # language of demirbank interface
    * CURRENCY_CODE = 417 # currency code for SOM
    * STORE_KEY = 'KEY VALUE RECEIVED FROM BANK'

  * Settings required for django Client and Balance external models:
    * DEMIR_BANK_CLIENT_MODEL_PATH = 'some_app.models' #for example
    * DEMIR_BANK_CLIENT_MODEL_NAME = 'Client' #for example
    * DEMIR_BANK_CLIENT_MODEL_SEARCH_FIELD = 'phone_number' #for example
    * DEMIR_BANK_CLIENT_MODEL_UPDATE_BALANCE_METHOD_NAME = 'update_balance' #for example