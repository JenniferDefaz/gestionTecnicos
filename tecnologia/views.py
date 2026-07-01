from django.shortcuts import render, redirect
from django.contrib import messages 
import os 
from .models import Tecnico, Curso, Inscripcion, Perfil 
#Estos son ára el login t el registro 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime




def loginVista(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            try:
                if usuario.perfil.rol == 'ADMIN':
                    return redirect('/listadoTecnicos/')
                else:
                    return redirect('/listadoInscripciones/')
            except:
                return redirect('/listadoTecnicos/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('/login/')
    return render(request, 'login.html')

def logoutVista(request):
    logout(request)
    return redirect('/login/')

def registroVista(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        cedula = request.POST['cedula']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        especialidad = request.POST['especialidad']
        foto = request.FILES.get('foto')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'registroTecnico.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso')
            return render(request, 'registroTecnico.html')
        if Tecnico.objects.filter(cedula=cedula).exists():
            messages.error(request, 'Ya existe un técnico registrado con esa cédula')
            return render(request, 'registroTecnico.html')
        if Tecnico.objects.filter(correo=correo).exists():
            messages.error(request, 'Ya existe un técnico registrado con ese correo')
            return render(request, 'registroTecnico.html')

        nuevoUsuario = User.objects.create_user(
            username=username,
            password=password1,
            email=correo
        )
        Perfil.objects.create(
            usuario=nuevoUsuario,
            rol='TECNICO'
        )
        Tecnico.objects.create(
            usuario=nuevoUsuario,
            nombres=nombres,
            apellidos=apellidos,
            cedula=cedula,
            correo=correo,
            telefono=telefono,
            especialidad=especialidad,
            foto=foto
        )
        messages.success(request, 'Registro exitoso, ya puedes iniciar sesión')
        return redirect('/login/')
    return render(request, 'registroTecnico.html')


def inicio(request):
    return render(request, 'inicio.html')



@login_required(login_url='/login/')
def nuevoTecnico(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    return render(request, 'registroTecnico.html')

@login_required(login_url='/login/')
def guardarTecnico(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    nombresNuevoTecnico = request.POST["nombres"]
    apellidosNuevoTecnico = request.POST["apellidos"]
    cedulaNuevoTecnico = request.POST["cedula"]
    correoNuevoTecnico = request.POST["correo"]
    telefonoNuevoTecnico = request.POST["telefono"]
    especialidadNuevoTecnico = request.POST["especialidad"]
    fotoNuevoTecnico = request.FILES.get("foto")

    if Tecnico.objects.filter(cedula=cedulaNuevoTecnico).exists():
        messages.error(request, 'Ya existe un técnico registrado con esa cédula')
        return redirect('/nuevoTecnico/')
    if Tecnico.objects.filter(correo=correoNuevoTecnico).exists():
        messages.error(request, 'Ya existe un técnico registrado con ese correo')
        return redirect('/nuevoTecnico/')

    Tecnico.objects.create(
        nombres=nombresNuevoTecnico,
        apellidos=apellidosNuevoTecnico,
        cedula=cedulaNuevoTecnico,
        correo=correoNuevoTecnico,
        telefono=telefonoNuevoTecnico,
        especialidad=especialidadNuevoTecnico,
        foto=fotoNuevoTecnico
    )
    messages.success(request, 'Técnico guardado exitosamente')
    return redirect('/listadoTecnicos/')

@login_required(login_url='/login/')
def listadoTecnicos(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    tecnicos = Tecnico.objects.all()
    return render(request, 'listadoTecnicos.html', {'misTecnicos': tecnicos})

@login_required(login_url='/login/')
def eliminarTecnico(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    tecnicoAEliminar = Tecnico.objects.get(id=id)
    if tecnicoAEliminar.foto:
        ruta_imagen = tecnicoAEliminar.foto.path
        if os.path.isfile(ruta_imagen):
            os.remove(ruta_imagen)
    tecnicoAEliminar.delete()
    messages.success(request, 'Técnico eliminado exitosamente')
    return redirect('/listadoTecnicos/')

@login_required(login_url='/login/')
def editarTecnico(request, id):
    tecnicoEditar = Tecnico.objects.get(id=id)
    if request.user.perfil.rol != 'ADMIN' and tecnicoEditar.usuario != request.user:
        return redirect('/listadoInscripciones/')
    return render(request, 'editarTecnico.html', {'tecnico': tecnicoEditar})

@login_required(login_url='/login/')
def actualizarTecnico(request, id):
    tecnicoActualizar = Tecnico.objects.get(id=id)
    if request.user.perfil.rol != 'ADMIN' and tecnicoActualizar.usuario != request.user:
        return redirect('/listadoInscripciones/')

    nom = request.POST['nombres']
    ape = request.POST['apellidos']
    ced = request.POST['cedula']
    cor = request.POST['correo']
    tel = request.POST['telefono']
    esp = request.POST['especialidad']

    if Tecnico.objects.filter(cedula=ced).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con esa cédula')
        return redirect(f'/editarTecnico/{id}/')
    if Tecnico.objects.filter(correo=cor).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con ese correo')
        return redirect(f'/editarTecnico/{id}/')

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

    if request.user.perfil.rol == 'ADMIN':
        messages.success(request, 'Técnico actualizado exitosamente')
        return redirect('/listadoTecnicos')
    else:
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('/miPerfil/')

@login_required(login_url='/login/')
def miPerfil(request):
    if request.user.perfil.rol == 'ADMIN':
        return redirect('/listadoTecnicos/')
    try:
        tecnicoActual = Tecnico.objects.get(usuario=request.user)
    except Tecnico.DoesNotExist:
        messages.error(request, 'No se encontró su perfil de técnico. Por favor, contacte al administrador.')
        return redirect('/login/')
    return render(request, 'miPerfil.html', {'tecnico': tecnicoActual})

@login_required(login_url='/login/')
def actualizarMiPerfil(request, id):
    if request.user.perfil.rol == 'ADMIN':
        return redirect('/listadoTecnicos/')
    nom = request.POST['nombres']
    ape = request.POST['apellidos']
    ced = request.POST['cedula']
    cor = request.POST['correo']
    tel = request.POST['telefono']
    esp = request.POST['especialidad']

    if Tecnico.objects.filter(cedula=ced).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con esa cédula')
        return redirect('/miPerfil/')
    if Tecnico.objects.filter(correo=cor).exclude(id=id).exists():
        messages.error(request, 'Ya existe otro técnico registrado con ese correo')
        return redirect('/miPerfil/')

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
    messages.success(request, 'Perfil actualizado exitosamente')
    return redirect('/miPerfil/')


# CURSO

@login_required(login_url='/login/')
def nuevoCurso(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    return render(request, 'registrarCursos.html')

@login_required(login_url='/login/')
def guardarCurso(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    nombreNuevoCurso = request.POST["nombre"]
    descripcionNuevoCurso = request.POST["descripcion"]
    instructorNuevoCurso = request.POST["instructor"]
    horasNuevoCurso = request.POST["horas_duracion"]
    fechaInicioNuevoCurso = request.POST["fecha_inicio"]
    fechaFinNuevoCurso = request.POST["fecha_fin"]

    # NUEVO: validar que la fecha fin sea posterior a la fecha inicio
    if fechaFinNuevoCurso <= fechaInicioNuevoCurso:
        messages.error(request, 'La fecha de fin debe ser posterior a la fecha de inicio')
        return redirect('/nuevoCurso/')

    Curso.objects.create(
        nombre=nombreNuevoCurso,
        descripcion=descripcionNuevoCurso,
        instructor=instructorNuevoCurso,
        horas_duracion=horasNuevoCurso,
        fecha_inicio=fechaInicioNuevoCurso,
        fecha_fin=fechaFinNuevoCurso
    )
    messages.success(request, 'Curso guardado exitosamente')
    return redirect('/listadoCursos/')

@login_required(login_url='/login/')
def listadoCursos(request):
    cursos = Curso.objects.all()
    return render(request, 'listadoCursos.html', {'misCursos': cursos})

@login_required(login_url='/login/')
def eliminarCurso(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    cursoAEliminar = Curso.objects.get(id=id)
    cursoAEliminar.delete()
    messages.success(request, 'Curso eliminado exitosamente')
    return redirect('/listadoCursos/')

@login_required(login_url='/login/')
def editarCurso(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    cursoEditar = Curso.objects.get(id=id)
    return render(request, 'editarCurso.html', {'curso': cursoEditar})

@login_required(login_url='/login/')
def actualizarCurso(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    nom = request.POST['nombre']
    des = request.POST['descripcion']
    ins = request.POST['instructor']
    hor = request.POST['horas_duracion']
    fin = request.POST['fecha_inicio']
    ffin = request.POST['fecha_fin']

    # NUEVO: validar fechas
    fechaInicioObj = datetime.strptime(fin, '%Y-%m-%d').date()
    fechaFinObj = datetime.strptime(ffin, '%Y-%m-%d').date()
    if fechaFinObj <= fechaInicioObj:
        messages.error(request, 'La fecha de fin debe ser posterior a la fecha de inicio')
        return redirect(f'/editarCurso/{id}/')

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


# INSCRIPCION (MATRICULA)


@login_required(login_url='/login/')
def registrarMatricula(request):
    if request.user.perfil.rol == 'ADMIN':
        return redirect('/listadoCursos/')
    try:
        tecnicoActual = Tecnico.objects.get(usuario=request.user)
    except Tecnico.DoesNotExist:
        messages.error(request, 'No se encontró su perfil de técnico. Por favor, contacte al administrador.')
        return redirect('/login/')
    cursos = Curso.objects.all()
    idsMatriculados = Inscripcion.objects.filter(tecnico=tecnicoActual).values_list('curso_id', flat=True)
    return render(request, 'registrarMatricula.html', {
        'misCursos': cursos,
        'idsMatriculados': list(idsMatriculados)
    })

@login_required(login_url='/login/')
def matricularCurso(request, id):
    if request.user.perfil.rol == 'ADMIN':
        return redirect('/listadoCursos/')
    try:
        tecnicoActual = Tecnico.objects.get(usuario=request.user)
    except Tecnico.DoesNotExist:
        messages.error(request, 'No se encontró su perfil de técnico. Por favor, contacte al administrador.')
        return redirect('/login/')

    cursoAMatricular = Curso.objects.get(id=id)

    if Inscripcion.objects.filter(tecnico=tecnicoActual, curso=cursoAMatricular).exists():
        messages.error(request, 'Ya está matriculado en este curso')
        return redirect('/registrarMatricula/')

    Inscripcion.objects.create(
        tecnico=tecnicoActual,
        curso=cursoAMatricular
    )
    messages.success(request, 'Matrícula registrada exitosamente')
    return redirect('/listadoInscripciones/')


@login_required(login_url='/login/')
def cancelarMatricula(request, id):
    if request.user.perfil.rol == 'ADMIN':
        return redirect('/listadoCursos/')
    try:
        tecnicoActual = Tecnico.objects.get(usuario=request.user)
        inscripcion = Inscripcion.objects.get(tecnico=tecnicoActual, curso_id=id)
    except (Tecnico.DoesNotExist, Inscripcion.DoesNotExist):
        messages.error(request, 'No se encontró la información solicitada.')
        return redirect('/registrarMatricula/')

    if inscripcion.estado != 'PENDIENTE':
        messages.error(request, 'No puede cancelar una inscripción ya evaluada')
        return redirect('/registrarMatricula/')

    inscripcion.delete()
    messages.success(request, 'Se canceló su matrícula exitosamente')
    return redirect('/registrarMatricula/')

@login_required(login_url='/login/')
def listadoInscripciones(request):
    if request.user.perfil.rol == 'ADMIN':
        inscripciones = Inscripcion.objects.all()
    else:
        try:
            tecnicoActual = Tecnico.objects.get(usuario=request.user)
            inscripciones = Inscripcion.objects.filter(tecnico=tecnicoActual)
        except Tecnico.DoesNotExist:
            messages.error(request, 'No se encontró su perfil de técnico. Por favor, contacte al administrador.')
            return redirect('/login/')
    return render(request, 'listadoInscripciones.html', {'misInscripciones': inscripciones})

@login_required(login_url='/login/')
def listadoTecnicosCursos(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    cursoActual = Curso.objects.get(id=id)
    inscripciones = Inscripcion.objects.filter(curso=cursoActual)
    return render(request, 'listadoTecnicosCursos.html', {'curso': cursoActual, 'misInscripciones': inscripciones})

@login_required(login_url='/login/')
def editarInscripcion(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    inscripcionEditar = Inscripcion.objects.get(id=id)
    return render(request, 'editarInscripcion.html', {'inscripcion': inscripcionEditar})

@login_required(login_url='/login/')
def actualizarInscripcion(request, id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('/listadoInscripciones/')
    nota = request.POST['nota_final']
    estado = request.POST['estado']
    inscripcionActualizar = Inscripcion.objects.get(id=id)
    inscripcionActualizar.nota_final = nota
    inscripcionActualizar.estado = estado
    inscripcionActualizar.save()
    messages.success(request, 'Inscripción actualizada exitosamente')
    return redirect(f'/listadoTecnicosCursos/{inscripcionActualizar.curso.id}/')

@login_required(login_url='/login/')
def certificado(request, id):
    inscripcionCertificado = Inscripcion.objects.get(id=id)
    if inscripcionCertificado.estado != 'APROBADO':
        messages.error(request, 'El certificado no está disponible para esta inscripción')
        return redirect('/listadoInscripciones/')
    return render(request, 'certificado.html', {'inscripcion': inscripcionCertificado})