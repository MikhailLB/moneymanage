# Generated by Django 5.1.3 on 2024-12-06 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temp_transactions', '0007_alter_temptransaction_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temptransaction',
            name='account',
        ),
    ]
