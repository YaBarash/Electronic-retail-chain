from django.contrib import admin
from retail_chain.models import Company, Product, Contacts


class ContactAdmin(admin.StackedInline):
    model = Contacts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_date',)


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
    inlines = [ContactAdmin]
