# Generated by Django 5.1.3 on 2024-12-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_transactions', '0006_alter_frequency_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temptransaction',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]