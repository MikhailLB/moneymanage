# Generated by Django 5.1.1 on 2024-10-05 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('budgets', '0002_alter_budget_options_and_more'),
        ('transactions', '0005_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Budget', 'verbose_name_plural': 'Budgets'},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(choices=[('income', 'Приход'), ('expense', 'Траты')], on_delete=django.db.models.deletion.CASCADE, to='transactions.transactionstype'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['-created_at'], name='transaction_created_300c15_idx'),
        ),
    ]
