# Generated by Django 5.1.4 on 2024-12-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retail_chain", "0005_alter_company_date_created_alter_company_debt"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Продукт", "verbose_name_plural": "Продукты"},
        ),
        migrations.AddField(
            model_name="company",
            name="products",
            field=models.ManyToManyField(
                to="retail_chain.product", verbose_name="Продукты"
            ),
        ),
    ]
