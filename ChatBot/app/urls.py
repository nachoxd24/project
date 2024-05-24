from django.urls import path
from .views import login_view,home,salir,chatbot,registro,lista_usuarios,editar_usuario,eliminar_usuario,\
  lista_cursos,agregar_asignatura,ver_contenidos_asignatura,agregar_contenido,ver_presentacion,\
  editar_contenido,eliminar_contenido,editar_curso,eliminar_curso,base,login_count_view,registro_admin



urlpatterns = [
  path('', base, name='base'),
  path('home/', home, name='home'),
  path('chabot/', chatbot, name='chatbot'),
  path('login/', login_view, name='login'),
  path('registro/', registro,name='registro'),
  path('salir/',salir , name='salir'),
  path('usuarios/', lista_usuarios, name='lista_usuarios'),
  path('usuarios/<int:pk>/editar/', editar_usuario, name='editar_usuario'),
  path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
  path('cursos/', lista_cursos, name='lista_cursos'),
  path('cursos/<int:curso_id>/agregar_asignatura/', agregar_asignatura, name='agregar_asignatura'),
  path('asignaturas/<int:asignatura_id>/', ver_contenidos_asignatura, name='ver_contenidos_asignatura'),
  path('asignaturas/<int:asignatura_id>/agregar_contenido/', agregar_contenido, name='agregar_contenido'),
  path('contenido/<int:contenido_id>/', ver_presentacion, name='ver_presentacion'),
  path('editar_contenido/<int:pk>/', editar_contenido, name='editar_contenido'),
  path('eliminar_contenido/<int:contenido_id>/', eliminar_contenido, name='eliminar_contenido'),
  path('cursos/<int:curso_id>/eliminar/', eliminar_curso, name='eliminar_curso'),
  path('cursos/<int:curso_id>/editar/', editar_curso, name='editar_curso'),
  path('login_count/', login_count_view, name='login_count'),
  path('registro_admin/', registro_admin, name='registro_admin'),
  

]