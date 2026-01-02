from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain')
    list_filter = ('name',)
    search_fields = ('name', 'domain')
    readonly_fields = ('id',)
