# Generated by Django 5.1.3 on 2024-11-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionstype',
            name='verbose_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]