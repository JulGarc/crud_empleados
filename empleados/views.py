from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employee

def login_view(request):
    if request.user.is_authenticated:
        return redirect("list_employees")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("list_employees")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "empleados/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def list_employees(request):
    q = request.GET.get('q', '').strip()
    filter_by = request.GET.get('filter_by', 'nombre')
    order_by_param = request.GET.get('order_by_param', 'nombre')

    valid_fields = ['nombre', 'cedula', 'email', 'fecha_nacimiento']
    if filter_by not in valid_fields:
        filter_by = 'nombre'
    if order_by_param not in valid_fields:
        order_by_param = 'nombre'

    employees = Employee.objects.all()
    if q:
        employees = employees.filter(**{f"{filter_by}__icontains": q})

 
    employees = employees.order_by(order_by_param)

    context = {
        'employees': employees,
        'search_query': q,
        'filter_by': filter_by,
        'order_by_param': order_by_param,
    }
    return render(request, 'empleados/list_employees.html', context)


@login_required
def create_employee(request):
    mensaje_exito = None
    errores_formulario = None  

    if request.method == 'POST':
        form = EmployeeForm(request.POST)  
        if form.is_valid():
            form.save()
            mensaje_exito = "Empleado creado exitosamente."
            form = EmployeeForm() 
        else:
            errores_formulario = form.errors  

    else:
        form = EmployeeForm()

    return render(request, 'empleados/employee_form.html', {
        'form': form,
        'mensaje_exito': mensaje_exito,
        'errores_formulario': errores_formulario,
        'accion': 'Crear empleado',
    })


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    mensaje_exito = None
    errores_formulario = None  

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            mensaje_exito = "Empleado actualizado exitosamente."
        else:
            errores_formulario = form.errors
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'empleados/employee_form.html', {
        'form': form,
        'mensaje_exito': mensaje_exito,
        'errores_formulario': errores_formulario,
        'accion': 'Editar',
    })
