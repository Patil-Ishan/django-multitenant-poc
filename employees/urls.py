from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_add, name='employee_add'),
    path('<int:pk>/', views.employee_view, name='employee_view'),
    path('<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('<int:pk>/add-role/', views.employee_add_role, name='employee_add_role'),
    path('role/<int:role_pk>/delete/', views.employee_role_delete, name='employee_role_delete'),
]