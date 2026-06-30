from django.shortcuts import render, redirect
from django.contrib import messages 
import os 
from .models import Tecnico, Curso, Inscripcion

# Create your views here.
def inicio(request):
    #Presentando en pantalla el contenido de inicio s
    return render(request, 'inicio.html')

def nuevoTecnico(request):
    return render(request, 'registroTecnico.html')

def guardarTecnico(request):
    #Capturando valores via metodo POST
    nombresNuevoTenico=request.POST["nombres"]
    apellidosNuevoTecnico=request.POST["apellidos"]
    cedulaNuevoTecnico=request.POST["cedula"]
    correoNuevoTecnico=request.POST["correo"]
    telefonoNuevoTecnico=request.POST["telefono"]
    especialidadNuevoTecnico=request.POST["especialidad"]
    #Capturando el archivo de neme=foto 
    fotoNuevoTecnico=request.FILES.get("foto")

    #iNSTANCIAR un objeto "Tecnico"
    nuevoTecnico=Tecnico.objects.create(
        nombres=nombresNuevoTenico,
        apellidos=apellidosNuevoTecnico,
        cedula=cedulaNuevoTecnico,
        correo=correoNuevoTecnico,
        telefono=telefonoNuevoTecnico,
        especialidad=especialidadNuevoTecnico,
        foto=fotoNuevoTecnico
    )

    messages.success(request, 'Registro exitoso') # Agregando un mensaje de éxito para mostrar en la plantilla después de crear el técnico
    return redirect('/listadoCursos/')

# ===========================================================================================================================
def listadoTecnicos(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'listadoTecnicos.html', {'misTecnicos': tecnicos})

# Eliminacion de un tecnico por id
def eliminarTecnico(request, id):
    tecnicoAEliminar = Tecnico.objects.get(id=id)
    if tecnicoAEliminar.foto:
        ruta_imagen = tecnicoAEliminar.foto.path
        if os.path.isfile(ruta_imagen):
            os.remove(ruta_imagen)
    tecnicoAEliminar.delete()
    messages.success(request, 'Técnico eliminado exitosamente')
    return redirect('/listadoTecnicos/')

# Ubicando el tecnico que se quiere editar con su ID
def editarTecnico(request, id):
    tecnicoEditar = Tecnico.objects.get(id=id)
    return render(request, 'editarTecnico.html', {'tecnico': tecnicoEditar})

# Actualizando el tecnico con los nuevos datos del formulario Esto es para validar
# un caso que al editar coloco la cedula de otro tecnico me lanza error 
# .exclude(id=id) es la clave: "busca si existe esa cédula/correo en algún OTRO técnico que no sea el que estoy editando ahora mismo".
def actualizarTecnico(request, id):
    nom = request.POST['nombres']
    ape = request.POST['apellidos']
    ced = request.POST['cedula']
    cor = request.POST['correo']
    tel = request.POST['telefono']
    esp = request.POST['especialidad']

    # Validamos que no exista otro tecnico (diferente a este) con la misma cedula o correo
    if Tecnico.objects.filter(cedula=ced).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con esa cédula')
        return redirect(f'/editarTecnico/{id}/')

    if Tecnico.objects.filter(correo=cor).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con ese correo')
        return redirect(f'/editarTecnico/{id}/')

    tecnicoActualizar = Tecnico.objects.get(id=id)
    tecnicoActualizar.nombres = nom
    tecnicoActualizar.apellidos = ape
    tecnicoActualizar.cedula = ced
    tecnicoActualizar.correo = cor
    tecnicoActualizar.telefono = tel
    tecnicoActualizar.especialidad = esp

    if request.FILES.get('foto'):
        if tecnicoActualizar.foto:
            ruta_imagen_anterior = tecnicoActualizar.foto.path
            if os.path.isfile(ruta_imagen_anterior):
                os.remove(ruta_imagen_anterior)
        tecnicoActualizar.foto = request.FILES['foto']

    tecnicoActualizar.save()
    messages.success(request, 'Técnico actualizado exitosamente')
    return redirect('/listadoTecnicos')




def nuevoCurso(request):
    return render(request, 'registrarCursos.html')

def guardarCurso(request):
    nombreNuevoCurso = request.POST["nombre"]
    descripcionNuevoCurso = request.POST["descripcion"]
    instructorNuevoCurso = request.POST["instructor"]
    horasNuevoCurso = request.POST["horas_duracion"]
    fechaInicioNuevoCurso = request.POST["fecha_inicio"]
    fechaFinNuevoCurso = request.POST["fecha_fin"]

    nuevoCurso = Curso.objects.create(
        nombre=nombreNuevoCurso,
        descripcion=descripcionNuevoCurso,
        instructor=instructorNuevoCurso,
        horas_duracion=horasNuevoCurso,
        fecha_inicio=fechaInicioNuevoCurso,
        fecha_fin=fechaFinNuevoCurso
    )

    messages.success(request, 'Curso guardado exitosamente')
    return redirect('/listadoCursos/')

def listadoCursos(request):
    cursos = Curso.objects.all()
    return render(request, 'listadoCursos.html', {'misCursos': cursos})

def eliminarCurso(request, id):
    cursoAEliminar = Curso.objects.get(id=id)
    cursoAEliminar.delete()
    messages.success(request, 'Curso eliminado exitosamente')
    return redirect('/listadoCursos/')

def editarCurso(request, id):
    cursoEditar = Curso.objects.get(id=id)
    return render(request, 'editarCurso.html', {'curso': cursoEditar})

def actualizarCurso(request, id):
    nom = request.POST['nombre']
    des = request.POST['descripcion']
    ins = request.POST['instructor']
    hor = request.POST['horas_duracion']
    fin = request.POST['fecha_inicio']
    ffin = request.POST['fecha_fin']

    cursoActualizar = Curso.objects.get(id=id)
    cursoActualizar.nombre = nom
    cursoActualizar.descripcion = des
    cursoActualizar.instructor = ins
    cursoActualizar.horas_duracion = hor
    cursoActualizar.fecha_inicio = fin
    cursoActualizar.fecha_fin = ffin
    cursoActualizar.save()

    messages.success(request, 'Curso actualizado exitosamente')
    return redirect('/listadoCursos')




# Pantalla del Técnico: ver cursos disponibles para matricularse
def registrarMatricula(request):
    cursos = Curso.objects.all()
    return render(request, 'registrarMatricula.html', {'misCursos': cursos})

# Guardar la matricula (el tecnico se inscribe a un curso)
def matricularCurso(request, id):
    cursoAMatricular = Curso.objects.get(id=id)
    tecnicoActual = Tecnico.objects.first()

    if Inscripcion.objects.filter(tecnico=tecnicoActual, curso=cursoAMatricular).exists():
        messages.error(request, 'Ya está matriculado en este curso')
        return redirect('/registrarMatricula/')

    Inscripcion.objects.create(tecnico=tecnicoActual, curso=cursoAMatricular)
    messages.success(request, 'Matrícula registrada exitosamente')
    return redirect('/listadoInscripciones/')

# Pantalla del Técnico: ver sus propias inscripciones/cursos
def listadoInscripciones(request):

    inscripciones = Inscripcion.objects.all()
    return render(request, 'listadoInscripciones.html', {'misInscripciones': inscripciones})

# Pantalla del Administrador: ver los tecnicos matriculados en un curso especifico
def listadoTecnicosCursos(request, id):
    cursoActual = Curso.objects.get(id=id)
    inscripciones = Inscripcion.objects.filter(curso=cursoActual)
    return render(request, 'listadoTecnicosCursos.html', {'curso': cursoActual, 'misInscripciones': inscripciones})

# Ubicando la inscripcion que se quiere editar (calificar) con su ID
def editarInscripcion(request, id):
    inscripcionEditar = Inscripcion.objects.get(id=id)
    return render(request, 'editarInscripcion.html', {'inscripcion': inscripcionEditar})


def actualizarInscripcion(request, id):
    nota = request.POST['nota_final']
    estado = request.POST['estado']

    inscripcionActualizar = Inscripcion.objects.get(id=id)
    inscripcionActualizar.nota_final = nota
    inscripcionActualizar.estado = estado
    inscripcionActualizar.save()

    messages.success(request, 'Inscripción actualizada exitosamente')
    return redirect(f'/listadoTecnicosCursos/{inscripcionActualizar.curso.id}/')

# Generar el certificado (solo si esta aprobado OJO)
def certificado(request, id):
    inscripcionCertificado = Inscripcion.objects.get(id=id)
    if inscripcionCertificado.estado != 'APROBADO':
        messages.error(request, 'El certificado no está disponible para esta inscripción')
        return redirect('/listadoInscripciones/')
    return render(request, 'certificado.html', {'inscripcion': inscripcionCertificado})

