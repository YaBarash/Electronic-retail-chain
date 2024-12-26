from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from requests import Response

from retail_chain.models import Company, Product, Contacts


class ContactAdmin(admin.StackedInline):
    model = Contacts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_date',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_type_display",
        "name",
        "supplier_link",
        "level",
        "date_created",
    )

    fields = (
        "name",
        "supplier",
        "level",
        "debt"
    )

    inlines = [ContactAdmin]

    @admin.display(description=('Link for supplier'))
    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse(f'admin:{obj.supplier._meta.app_label}_{obj.supplier._meta.model_name}_change',
                          args=(obj.supplier.pk,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.supplier}</a>')
        return '-'
    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'city':
    #         kwargs['queryset'] = Contacts.objects.filter(applicable=False)

    # @admin.action
    # def make_published(CompanyAdmin, request, queryset):
    #     queryset.update(debt=0)
