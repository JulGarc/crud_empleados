from django.urls import path
from .views import login_view, logout_view, create_employee, list_employees, edit_employee

urlpatterns = [
    path('', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),  
    path('empleados/', list_employees, name='list_employees'),  
    path('empleados/crear/', create_employee, name='create_employee'),
    path('editar/<int:employee_id>/', edit_employee, name='edit_employee'),
]
