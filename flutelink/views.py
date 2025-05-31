from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UsuarioDisciplina
from .forms import UsuarioDisciplinaForm
from .models import Disciplina, UsuarioDisciplina, UsuarioDisciplinaTipo
from .models import Cantante, Bailarin, Grafitero, Instrumentista, Productor
from .forms import CantanteForm, BailarinForm, GrafiteroForm, InstrumentistaForm, ProductorForm
from .utils import calcular_compatibilidad

User = get_user_model()

@login_required
def registro_colaboracion(request):
    form_map = {
        'cantante': CantanteForm,
        'bailarin': BailarinForm,
        'grafitero': GrafiteroForm,  # <-- asegúrate de que el nombre coincide
        'instrumentista': InstrumentistaForm,
        'productor': ProductorForm
    }

    if request.method == 'POST' and 'disciplina' in request.POST:
        disciplina_id = request.POST.get('disciplina')
        disciplina = Disciplina.objects.get(id=disciplina_id)

        usuario_disciplina, _ = UsuarioDisciplina.objects.get_or_create(
            usuario=request.user,
            disciplina=disciplina
        )

        request.session['usuario_disciplina_id'] = usuario_disciplina.id
        return redirect('registro_colaboracion')

    elif request.method == 'POST':
        usuario_disciplina_id = request.session.get('usuario_disciplina_id')
        if not usuario_disciplina_id:
            return redirect('form_disciplina')

        usuario_disciplina = UsuarioDisciplina.objects.get(id=usuario_disciplina_id)
        disciplina_nombre = usuario_disciplina.disciplina.nombre.lower()

        if UsuarioDisciplinaTipo.objects.filter(usuario_disciplina=usuario_disciplina, tipo=disciplina_nombre).exists():
            return render(request, 'ya_enviado.html', {'disciplina': usuario_disciplina.disciplina})

        form_class = form_map.get(disciplina_nombre)
        if not form_class:
            return HttpResponse(f"Formulario no disponible para la disciplina {disciplina_nombre}", status=400)

        form = form_class(request.POST)
        if form.is_valid():
            tipo = UsuarioDisciplinaTipo.objects.create(
                usuario_disciplina=usuario_disciplina,
                tipo=disciplina_nombre
            )
            instancia = form.save(commit=False)
            instancia.usuario_disciplina_tipo = tipo
            instancia.save()

            del request.session['usuario_disciplina_id']
            return redirect('mostrar_coincidencias')

        return render(request, 'colaboracion.html', {'form': form, 'disciplina': usuario_disciplina.disciplina})

    else:
        usuario_disciplina_id = request.session.get('usuario_disciplina_id')
        if usuario_disciplina_id:
            usuario_disciplina = UsuarioDisciplina.objects.get(id=usuario_disciplina_id)
            disciplina_nombre = usuario_disciplina.disciplina.nombre.lower()

            if UsuarioDisciplinaTipo.objects.filter(usuario_disciplina=usuario_disciplina, tipo=disciplina_nombre).exists():
                return render(request, 'ya_enviado.html', {'disciplina': usuario_disciplina.disciplina})

            form_class = form_map.get(disciplina_nombre)
            if not form_class:
                return HttpResponse(f"Formulario no disponible para la disciplina {disciplina_nombre}", status=400)

            form = form_class()
            return render(request, 'colaboracion.html', {'form': form, 'disciplina': usuario_disciplina.disciplina})

        disciplinas = Disciplina.objects.all()
        return render(request, 'form_disciplina.html', {'disciplinas': disciplinas})


@login_required
def mostrar_coincidencias(request):
    user = request.user

    try:
        usuario_tipo = UsuarioDisciplinaTipo.objects.filter(
            usuario_disciplina__usuario=user
        ).latest('usuario_disciplina__id')
    except UsuarioDisciplinaTipo.DoesNotExist:
        return render(request, 'coincidencias.html', {'error': 'No has registrado una disciplina aún.'})

    tipo_disciplina = usuario_tipo.tipo.lower()
    mi_disciplina_id = usuario_tipo.usuario_disciplina.disciplina.id

    modelos = {
        'cantante': Cantante,
        'bailarin': Bailarin,
        'grafitero': Grafitero,
        'instrumentista': Instrumentista,
        'productor': Productor,
    }

    ModeloActual = modelos.get(tipo_disciplina)
    if not ModeloActual:
        return render(request, 'coincidencias.html', {'error': 'Disciplina no reconocida.'})

    try:
        mi_instancia = ModeloActual.objects.get(usuario_disciplina_tipo=usuario_tipo)
    except ModeloActual.DoesNotExist:
        return render(request, 'coincidencias.html', {'error': 'No se encontró tu perfil para esta disciplina.'})

    # Parsear lista de IDs de disciplinas que busca este usuario
    busca_mia_ids = [int(b) for b in (mi_instancia.busca or "").split(',') if b.strip().isdigit()]

    coincidencias = []

    for nombre_modelo, Modelo in modelos.items():
        if nombre_modelo == tipo_disciplina:
            continue

        for obj in Modelo.objects.select_related('usuario_disciplina_tipo__usuario_disciplina__usuario'):
            obj_disciplina_id = obj.usuario_disciplina_tipo.usuario_disciplina.disciplina.id
            busca_obj_ids = [int(b) for b in (obj.busca or "").split(',') if b.strip().isdigit()]

            # Comparar usando IDs: ¿yo busco su disciplina? ¿él/ella busca la mía?
            if mi_disciplina_id in busca_obj_ids and obj_disciplina_id in busca_mia_ids:
                compat = calcular_compatibilidad(mi_instancia, obj)
                coincidencias.append((obj, compat, nombre_modelo))

    coincidencias.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'coincidencias.html', {
        'coincidencias': coincidencias,
        'mi_disciplina': tipo_disciplina.capitalize()
    })


@login_required
def verificar_registro(request):
    user = request.user
    try:
        UsuarioDisciplinaTipo.objects.filter(usuario_disciplina__usuario=user).latest('usuario_disciplina__id')
        return redirect('mostrar_coincidencias')
    except UsuarioDisciplinaTipo.DoesNotExist:
        return render(request, 'no_registro.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.disciplina = request.POST.get('disciplina', user.disciplina)
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('user_profile')

    return render(request, 'user_profile.html', {'user': request.user})

@login_required
def seleccionar_disciplina(request):
    # Verificar si ya existe una entrada para este usuario
    if UsuarioDisciplina.objects.filter(usuario=request.user).exists():
        return render(request, 'ya_enviado.html')

    if request.method == 'POST':
        form = UsuarioDisciplinaForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.usuario = request.user  # Aseguramos que se guarda con el usuario actual
            instancia.save()
            return render(request, 'ya_enviado.html')
    else:
        form = UsuarioDisciplinaForm()

    return render(request, 'seleccionar_disciplina.html', {'form': form})