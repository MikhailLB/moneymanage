# Generated by Django 5.1.3 on 2024-12-05 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temp_transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temptransaction',
            old_name='updated_at',
            new_name='call_time',
        ),
    ]
