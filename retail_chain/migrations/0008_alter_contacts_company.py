# Generated by Django 5.1.4 on 2024-12-21 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retail_chain", "0007_contacts_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contacts",
            name="company",
            field=models.ForeignKey(
                help_text="Укажите компанию",
                on_delete=django.db.models.deletion.CASCADE,
                to="retail_chain.company",
                verbose_name="Компания",
            ),
        ),
    ]
