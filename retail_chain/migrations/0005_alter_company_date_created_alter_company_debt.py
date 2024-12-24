# Generated by Django 5.1.4 on 2024-12-21 19:41

import djmoney.models.fields
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "retail_chain",
            "0004_contacts_product_company_date_created_company_debt_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="company",
            name="debt",
            field=djmoney.models.fields.MoneyField(
                decimal_places=2,
                default=Decimal("0.0"),
                default_currency="RUB",
                help_text="Укажите задолженость вашему поставщику",
                max_digits=14,
                verbose_name="Задолженость",
            ),
        ),
    ]