from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'email', 'phone', 'city', 'created_at')
    search_fields = ('name', 'company_name', 'email', 'phone', 'city')
    filter_horizontal = ('clients',)
    readonly_fields = ('created_at', 'updated_at')
