# Generated by Django 5.1.3 on 2024-12-09 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_account_currency'),
        ('transactions', '0014_alter_transaction_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
    ]
