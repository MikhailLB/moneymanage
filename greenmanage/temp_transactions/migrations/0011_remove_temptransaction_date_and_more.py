# Generated by Django 5.1.3 on 2024-12-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_transactions', '0010_remove_temptransaction_last_processed_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temptransaction',
            name='date',
        ),
        migrations.AddField(
            model_name='temptransaction',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]