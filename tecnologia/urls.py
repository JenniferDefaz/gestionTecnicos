from django.urls import path  
from . import views
from django.contrib import messages


urlpatterns = [
    path('', views.inicio),
    path('nuevoTecnico/', views.nuevoTecnico),
    path('guardarTecnico/', views.guardarTecnico),
    path('listadoTecnicos/', views.listadoTecnicos),
    path('eliminarTecnico/<int:id>/', views.eliminarTecnico),
    path('editarTecnico/<int:id>/', views.editarTecnico),
    path('actualizarTecnico/<int:id>/', views.actualizarTecnico),

   
    path('nuevoCurso/', views.nuevoCurso),
    path('guardarCurso/', views.guardarCurso),
    path('listadoCursos/', views.listadoCursos),
    path('eliminarCurso/<int:id>/', views.eliminarCurso),
    path('editarCurso/<int:id>/', views.editarCurso),
    path('actualizarCurso/<int:id>/', views.actualizarCurso),

    path('registrarMatricula/', views.registrarMatricula),
    path('matricularCurso/<int:id>/', views.matricularCurso),
    path('listadoInscripciones/', views.listadoInscripciones),
    path('listadoTecnicosCursos/<int:id>/', views.listadoTecnicosCursos),
    path('editarInscripcion/<int:id>/', views.editarInscripcion),
    path('actualizarInscripcion/<int:id>/', views.actualizarInscripcion),

    path('certificado/<int:id>/', views.certificado),

]


