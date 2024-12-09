# Generated by Django 5.1.3 on 2024-12-09 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_alter_budget_user'),
        ('reminders', '0002_reminders_budget_alter_reminders_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminders',
            name='budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='budgets.budget'),
        ),
    ]
