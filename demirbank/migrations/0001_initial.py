# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemirBankPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=255)),
                ('added', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('auth_code', models.CharField(default=b'', max_length=12)),
                ('extra_cardbrand', models.CharField(default=b'', max_length=128)),
                ('extra_trxdate', models.DateTimeField(null=True)),
                ('err_msg', models.CharField(default=b'', max_length=255)),
                ('hash', models.CharField(default=b'', max_length=255)),
                ('hash_params', models.CharField(default=b'', max_length=255)),
                ('hash_params_val', models.CharField(default=b'', max_length=255)),
                ('host_ref_num', models.CharField(default=b'', max_length=50)),
                ('masked_pan', models.CharField(default=b'', max_length=50)),
                ('pa_res_syntax_ok', models.BooleanField(default=False)),
                ('pa_res_verified', models.BooleanField(default=False)),
                ('proc_return_code', models.CharField(default=b'', max_length=2)),
                ('response', models.CharField(default=b'', max_length=50)),
                ('return_oid', models.IntegerField(default=0)),
                ('trans_id', models.CharField(default=b'', max_length=64)),
                ('amount', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('cavv', models.CharField(default=b'', max_length=28)),
                ('client_id', models.CharField(default=b'', max_length=15)),
                ('currency', models.PositiveSmallIntegerField(default=0)),
                ('eci', models.CharField(default=b'', max_length=2)),
                ('md', models.CharField(default=b'', max_length=512)),
                ('rnd', models.CharField(default=b'', max_length=50)),
                ('md_error_msg', models.CharField(default=b'', max_length=512)),
                ('md_status', models.PositiveSmallIntegerField(default=0)),
                ('merchant_id', models.CharField(default=b'', max_length=50)),
                ('oid', models.IntegerField(default=0)),
                ('storetype', models.CharField(default=b'', max_length=255)),
                ('txstatus', models.CharField(default=b'', max_length=15)),
                ('client_ip', models.GenericIPAddressField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
