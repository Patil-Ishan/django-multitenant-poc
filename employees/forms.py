from django import forms
from easy_tenants.utils import get_current_tenant
from .models import Employee, EmployeeAddress, EmployeeRole

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['emp_code', 'name', 'email']
    
    def clean_emp_code(self):
        emp_code = self.cleaned_data.get('emp_code')
        current_tenant = get_current_tenant()
        
        if current_tenant and emp_code:
            query = Employee.objects.filter(tenant=current_tenant, emp_code=emp_code)
            
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise forms.ValidationError(
                    f"Employee code '{emp_code}' already exists for this tenant. Please use a different code."
                )
        
        return emp_code

class EmployeeAddressForm(forms.ModelForm):
    class Meta:
        model = EmployeeAddress
        fields = ['city', 'state']

class EmployeeRoleForm(forms.ModelForm):
    class Meta:
        model = EmployeeRole
        fields = ['role']
