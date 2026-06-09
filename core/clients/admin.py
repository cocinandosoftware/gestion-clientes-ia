from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'email', 'phone', 'city', 'created_at')
    search_fields = ('name', 'company_name', 'email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')
