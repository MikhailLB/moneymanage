# Generated by Django 5.1.1 on 2024-10-02 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(choices=[('1', 'income'), ('2', 'expense')], on_delete=django.db.models.deletion.CASCADE, to='transactions.transactionstype'),
        ),
    ]
