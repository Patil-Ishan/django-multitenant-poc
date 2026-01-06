from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeViewSet.as_view({'get': 'list'}), name='employee_list'),
    path('add/', views.EmployeeViewSet.as_view({'get': 'create', 'post': 'create'}), name='employee_add'),
    path('<int:pk>/', views.EmployeeViewSet.as_view({'get': 'retrieve'}), name='employee_view'),
    path('<int:pk>/edit/', views.EmployeeViewSet.as_view({'get': 'update', 'post': 'update'}), name='employee_edit'),
    path('<int:pk>/delete/', views.EmployeeViewSet.as_view({'get': 'destroy', 'post': 'destroy'}), name='employee_delete'),
    path('<int:pk>/add-role/', views.EmployeeViewSet.as_view({'get': 'add_role', 'post': 'add_role'}), name='employee_add_role'),
    path('role/<int:pk>/delete/', views.EmployeeRoleViewSet.as_view({'get': 'destroy', 'post': 'destroy'}), name='employee_role_delete'),
]