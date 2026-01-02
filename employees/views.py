from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from easy_tenants.utils import get_current_tenant
from .models import Employee, EmployeeAddress, EmployeeRole
from .forms import EmployeeForm, EmployeeAddressForm, EmployeeRoleForm

def employee_list(request):
    """List all employees for the current tenant"""
    employees = Employee.objects.all().order_by('name')
    return render(request, 'employees/list.html', {'employees': employees})

def employee_view(request, pk):
    """View employee details with addresses and roles"""
    employee = get_object_or_404(Employee, pk=pk)
    addresses = employee.addresses.all()
    roles = employee.roles.all()
    
    return render(request, 'employees/view.html', {
        'employee': employee,
        'addresses': addresses,
        'roles': roles,
    })

def employee_add(request):
    """Add a new employee with address"""
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

def employee_edit(request, pk):
    """Edit an existing employee"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        return redirect('employees:employee_list')
    
    employee = get_object_or_404(Employee, pk=pk)
    
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

def employee_delete(request, pk):
    """Delete an employee"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        try:
            employee.delete()
            return redirect('employees:employee_list')
        except Exception:
            return redirect('employees:employee_list')
    
    return render(request, 'employees/delete.html', {'employee': employee})

def employee_add_role(request, pk):
    """Add a role to an employee"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        return redirect('employees:employee_list')
    
    employee = get_object_or_404(Employee, pk=pk)
    
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

def employee_role_delete(request, role_pk):
    """Delete a role from an employee"""
    role = get_object_or_404(EmployeeRole, pk=role_pk)
    employee_pk = role.employee.pk
    
    if request.method == 'POST':
        try:
            role.delete()
            return redirect('employees:employee_view', pk=employee_pk)
        except Exception:
            return redirect('employees:employee_list')
    
    return render(request, 'employees/delete_role.html', {'role': role})
