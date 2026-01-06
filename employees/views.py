from django.shortcuts import render, redirect
from easy_tenants.utils import get_current_tenant
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Employee, EmployeeRole
from .forms import EmployeeForm, EmployeeAddressForm, EmployeeRoleForm


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for Employee CRUD operations"""
    
    def get_queryset(self):
        return Employee.objects.all().order_by('name')
    
    def list(self, request, *args, **kwargs):
        """List all employees - renders HTML template"""
        employees = self.get_queryset()
        return render(request, 'employees/list.html', {'employees': employees})
    
    def retrieve(self, request, *args, **kwargs):
        """View employee details with addresses and roles - renders HTML template"""
        employee = self.get_object()
        addresses = employee.addresses.all()
        roles = employee.roles.all()
        
        return render(request, 'employees/view.html', {
            'employee': employee,
            'addresses': addresses,
            'roles': roles,
        })
    
    def create(self, request, *args, **kwargs):
        """Create a new employee - renders HTML template"""
        current_tenant = get_current_tenant()
        if not current_tenant:
            return redirect('employees:employee_list')
        
        if request.method == 'POST':
            employee_form = EmployeeForm(request.POST)
            address_form = EmployeeAddressForm(request.POST)
            
            if employee_form.is_valid() and address_form.is_valid():
                try:
                    employee = employee_form.save(commit=False)
                    employee.tenant = current_tenant
                    employee.save()
                    
                    address = address_form.save(commit=False)
                    address.tenant = current_tenant
                    address.employee = employee
                    address.save()
                    
                    return redirect('employees:employee_view', pk=employee.pk)
                except Exception:
                    return redirect('employees:employee_list')
        else:
            employee_form = EmployeeForm()
            address_form = EmployeeAddressForm()
        
        return render(request, 'employees/add.html', {
            'employee_form': employee_form,
            'address_form': address_form,
        })
    
    def update(self, request, *args, **kwargs):
        """Update an employee - renders HTML template"""
        current_tenant = get_current_tenant()
        if not current_tenant:
            return redirect('employees:employee_list')
        
        employee = self.get_object()
        
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('employees:employee_view', pk=employee.pk)
                except Exception:
                    return redirect('employees:employee_list')
        else:
            form = EmployeeForm(instance=employee)
        
        return render(request, 'employees/edit.html', {
            'form': form,
            'employee': employee,
        })
    
    def destroy(self, request, *args, **kwargs):
        """Delete an employee - renders HTML template"""
        employee = self.get_object()
        
        if request.method == 'POST':
            try:
                employee.delete()
                return redirect('employees:employee_list')
            except Exception:
                return redirect('employees:employee_list')
        
        return render(request, 'employees/delete.html', {'employee': employee})
    
    @action(detail=True, methods=['get', 'post'], url_path='add-role')
    def add_role(self, request, pk=None):
        """Add a role to an employee - renders HTML template"""
        current_tenant = get_current_tenant()
        if not current_tenant:
            return redirect('employees:employee_list')
        
        employee = self.get_object()
        
        if request.method == 'POST':
            form = EmployeeRoleForm(request.POST)
            if form.is_valid():
                try:
                    role = form.save(commit=False)
                    role.tenant = current_tenant
                    role.employee = employee
                    role.save()
                    return redirect('employees:employee_view', pk=employee.pk)
                except Exception:
                    return redirect('employees:employee_list')
        else:
            form = EmployeeRoleForm()
        
        return render(request, 'employees/add_role.html', {
            'form': form,
            'employee': employee,
        })


class EmployeeRoleViewSet(viewsets.ModelViewSet):
    """ViewSet for EmployeeRole operations"""
    
    def get_queryset(self):
        return EmployeeRole.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        """Delete a role - renders HTML template"""
        role = self.get_object()
        employee_pk = role.employee.pk
        
        if request.method == 'POST':
            try:
                role.delete()
                return redirect('employees:employee_view', pk=employee_pk)
            except Exception:
                return redirect('employees:employee_list')
        
        return render(request, 'employees/delete_role.html', {'role': role})
