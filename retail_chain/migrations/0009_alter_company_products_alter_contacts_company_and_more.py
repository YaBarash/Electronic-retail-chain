# Generated by Django 5.1.4 on 2024-12-27 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retail_chain", "0008_alter_contacts_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="products",
            field=models.ManyToManyField(
                help_text="Укажите продукты, которые предоставляет компания",
                to="retail_chain.product",
                verbose_name="Продукты",
            ),
        ),
        migrations.AlterField(
            model_name="contacts",
            name="company",
            field=models.ForeignKey(
                help_text="Укажите компанию",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_contacts",
                to="retail_chain.company",
                verbose_name="Компания",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_model",
            field=models.CharField(
                help_text="Укажите модель продукта",
                max_length=150,
                unique=True,
                verbose_name="Модель продукта",
            ),
        ),
    ]
