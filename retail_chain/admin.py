from django.contrib import admin

from retail_chain.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "get_type_display",
        "name",
        "supplier",
        "level",
        "date_created",
        "debt",
    )
