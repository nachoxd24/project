from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso, Asignatura,Contenido,LoginCount
from .forms import CursoForm, AsignaturaForm,ContenidoForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    return render(request,'app/home.html')

def base(request):
    return render(request,'app/base.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirecciona a una página de éxito o a donde desees
            return redirect('dashboard')
        else:
            # Manejar la lógica para un inicio de sesión fallido
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
@permission_required('app.view_logincount')
def login_count_view(request):
    users_with_counts = []
    users = User.objects.all()

    for user in users:
        login_count, created = LoginCount.objects.get_or_create(user=user)
        users_with_counts.append({'user': user, 'login_count': login_count.count})

    paginator = Paginator(users_with_counts, 5)  # 5 usuarios por página
    page_number = request.GET.get('page', 1)

    try:
        users_with_counts = paginator.page(page_number)
    except:
        users_with_counts = paginator.page(paginator.num_pages)

    return render(request, 'registration/login_count.html', {'users_with_counts': users_with_counts})

def registro(request):
    data ={
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password =formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has Registrado Correctamente")
            return redirect(to="chatbot")
        data["form"] = formulario
    return render(request, 'registration/registro.html' , data )

def registro_admin(request):
    data ={
        'form': CustomUserCreationForm(),
        'curso_permissions': Permission.objects.filter(content_type=ContentType.objects.get_for_model(Curso)),
        'asignatura_permissions': Permission.objects.filter(content_type=ContentType.objects.get_for_model(Asignatura)),
        'contenido_permissions': Permission.objects.filter(content_type=ContentType.objects.get_for_model(Contenido))
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save(commit=False)
            user.set_password(formulario.cleaned_data["password1"])
            user.save()
            messages.success(request, "Te has Registrado Correctamente")

            # Manejar permisos seleccionados
            permisos_seleccionados = formulario.cleaned_data.get('permisos', [])
            user.user_permissions.set(permisos_seleccionados)

            return redirect(to="lista_usuarios")
        data["form"] = formulario
    return render(request, 'registration/registro_admin.html', data)

@permission_required('app.view_user_list')
def lista_usuarios(request):
    usuarios = User.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator= Paginator(usuarios, 5)
        usuarios = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': usuarios,
        'paginator':paginator
    }
    return render(request, 'admin/lista_usuarios.html', data)

def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'admin/editar_usuario.html', {'usuario': usuario})

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'admin/eliminar_usuario.html', {'usuario': usuario})

def salir(request):
    logout(request)
    return redirect('home')


def chatbot(request):
    cursos = Curso.objects.all()
    return render(request,'app/chatbot.html', {'cursos': cursos})

@login_required
def lista_cursos(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cursos')  # Redirige a la misma página para mostrar la lista actualizada
    else:
        form = CursoForm()

    cursos = Curso.objects.all()
    context = {'cursos': cursos, 'form': form}
    return render(request, 'app/lista_cursos.html', context)

@permission_required('app.change_curso')
def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm(instance=curso)

    cursos = Curso.objects.all()
    return render(request, 'admin/editar_curso.html', {'curso':curso, 'cursos':cursos , 'form': form})

@permission_required('app.delete_curso')
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    
    if request.method == 'POST':
        # Si se confirma la eliminación
        curso.delete()
        return redirect('lista_cursos')
    else:
        # Si se accede a la vista directamente, renderiza la página de confirmación de eliminación
        cursos = Curso.objects.all() 
        return render(request, 'admin/eliminacion_curso.html', {'curso': curso, 'cursos': cursos})


def agregar_asignatura(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            asignatura = form.save(commit=False)
            asignatura.curso_id = curso_id
            asignatura.save()
            return redirect('agregar_asignatura', curso_id=curso_id)
    else:
        form = AsignaturaForm()

    cursos = Curso.objects.all()
    return render(request, 'admin/agregar_asignatura.html', {'cursos':cursos, 'curso':curso, 'form': form})


def ver_contenidos_asignatura(request, asignatura_id):

    if request.method == 'POST':
        # Si se envía el formulario de confirmación
        contenidos.delete()
        return redirect('ver_contenidos_asignatura', asignatura_id=asignatura_id)

    cursos = Curso.objects.all()
    asignatura = Asignatura.objects.get(id=asignatura_id)
    contenidos = asignatura.contenidos.all()
    return render(request, 'app/ver_contenidos_asignatura.html', {'asignatura': asignatura, 'contenidos': contenidos, 'cursos': cursos})

def agregar_contenido(request, asignatura_id):
    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.asignatura_id = asignatura_id
            contenido.save()
            return redirect('ver_contenidos_asignatura', asignatura_id=asignatura_id)
    else:
        form = ContenidoForm()
    cursos = Curso.objects.all() 
    return render(request, 'admin/agregar_contenido.html', {'cursos':cursos, 'form': form})

def ver_presentacion(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    fs = FileSystemStorage()
    url_presentacion = fs.url(contenido.presentacion.name)
    return render(request, 'app/ver_presentacion.html', {'url_presentacion': url_presentacion})


def editar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    asignatura_id = contenido.asignatura_id

    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES, instance=contenido)
        if form.is_valid():
            form.save()
            return redirect('ver_contenidos_asignatura', asignatura_id=asignatura_id)
    else:
        form = ContenidoForm(instance=contenido)

    cursos = Curso.objects.all()
    return render(request, 'admin/editar_contenido.html', {'cursos':cursos,'form': form})


def eliminar_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    asignatura_id = contenido.asignatura_id
    
    if request.method == 'POST':
        # Si se envía el formulario de confirmación
        contenido.delete()
        return redirect('ver_contenidos_asignatura', asignatura_id=asignatura_id)
    else:
        # Si se accede a la vista directamente, renderiza el formulario de confirmación
        cursos = Curso.objects.all()
        return render(request, 'admin/eliminar_contenido.html', {'cursos':cursos, 'contenido': contenido})


