from django.contrib import admin
from .models import Employee, EmployeeAddress, EmployeeRole

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_code', 'name', 'email', 'tenant')
    list_filter = ('tenant',)
    search_fields = ('emp_code', 'name', 'email')
    readonly_fields = ('tenant',)

@admin.register(EmployeeAddress)
class EmployeeAddressAdmin(admin.ModelAdmin):
    list_display = ('employee', 'city', 'state', 'tenant')
    list_filter = ('tenant', 'state')
    search_fields = ('employee__name', 'city', 'state')
    readonly_fields = ('tenant',)

@admin.register(EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'role', 'tenant')
    list_filter = ('tenant', 'role')
    search_fields = ('employee__name', 'role')
    readonly_fields = ('tenant',)
