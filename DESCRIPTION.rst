Library django-demirbank
=======================

Supports only one operation "Selling" (type `Auth`) which includes `Pre-Auth` and `Post-Auth`
Supported only following settings
``STORE_TYPE = '3d_Pay_Hosting'``
``TRANSACTION_TYPE = 'Auth'``

Library settings
================

The following settings needs to add inside ``settings/dev.py`` or ``settings/prod.py``

=======================================================  ==================================================
Name                                                     Value
=======================================================  ==================================================
DEMIR_BANK_PAY_ACTION_URL                                'url/to/demirbank/proces'
DEMIR_BANK_CLIENT_ID                                     12345678 # client id
DEMIR_BANK_TRANSACTION_TYPE                              'Auth' # type for Selling operation
DEMIR_BANK_INSTALMENT                                    '' # empty string for this parameter
DEMIR_BANK_OK_URL                                        'url/to/merchant/success/page'
DEMIR_BANK_FAIL_URL                                      'url/to/merchant/error/page'
DEMIR_BANK_STORE_TYPE                                    '3d_Pay_Hosting'
DEMIR_BANK_LANG                                          'ru' # language of demirbank interface
DEMIR_BANK_CURRENCY_CODE                                 417 # currency code for SOM
DEMIR_BANK_STORE_KEY                                     'KEY VALUE RECEIVED FROM BANK'
``DEMIR_BANK_CLIENT_MODEL_PATH``                         'some_app.models' #for example
``DEMIR_BANK_CLIENT_MODEL_NAME``                         'Client' #for example
``DEMIR_BANK_CLIENT_MODEL_SEARCH_FIELD``                 'phone_number' #for example
``DEMIR_BANK_CLIENT_MODEL_UPDATE_BALANCE_METHOD_NAME``   'update_balance' #for example
``DEMIR_BANK_DATABASE_CONNECTION_NAME``                  needed for using inside transaction.atomic(using=)
=======================================================  ==================================================
