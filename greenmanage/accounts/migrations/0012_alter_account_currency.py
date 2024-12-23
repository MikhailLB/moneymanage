# Generated by Django 5.1.3 on 2024-12-09 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_account_currency'),
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='currencies.currency'),
        ),
    ]
