# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_name', models.CharField(max_length=20)),
                ('u_pwd', models.CharField(max_length=40)),
                ('u_phone', models.CharField(max_length=11)),
                ('u_get', models.CharField(max_length=20)),
                ('u_address', models.CharField(max_length=100)),
                ('u_zip', models.CharField(max_length=6)),
                ('u_email', models.CharField(max_length=40)),
                ('u_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
