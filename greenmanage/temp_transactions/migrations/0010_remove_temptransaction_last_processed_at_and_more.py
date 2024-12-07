# Generated by Django 5.1.3 on 2024-12-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_transactions', '0009_temptransaction_last_processed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temptransaction',
            name='last_processed_at',
        ),
        migrations.AddField(
            model_name='temptransaction',
            name='last_processed',
            field=models.DateField(blank=True, null=True),
        ),
    ]
