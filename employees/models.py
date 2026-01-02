from django.db import models
from easy_tenants.models import TenantManager, TenantAwareAbstract
from core.models import Tenant

class Employee(TenantAwareAbstract):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    emp_code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    objects = TenantManager()
    
    class Meta:
        db_table = 'employees'
        unique_together = [['tenant', 'emp_code']]
    
    def __str__(self):
        return f"{self.name} ({self.emp_code})"

class EmployeeAddress(TenantAwareAbstract):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    objects = TenantManager()
    
    class Meta:
        db_table = 'employee_addresses'
    
    def __str__(self):
        return f"{self.employee.name} - {self.city}, {self.state}"

class EmployeeRole(TenantAwareAbstract):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=100)
    
    objects = TenantManager()
    
    class Meta:
        db_table = 'employee_roles'
        unique_together = [['tenant', 'employee', 'role']]
    
    def __str__(self):
        return f"{self.employee.name} - {self.role}"
