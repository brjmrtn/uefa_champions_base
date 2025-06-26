from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import Fase, Partido, Prediccion, PerfilUsuario
from .utils import actualizar_fases_automaticamente, calcular_puntos
from .forms import PrediccionBonusForm
from .models import PrediccionBonus
from .utils import calcular_puntos, puntos_por_bonus
from django.http import HttpResponse
import csv


@login_required
def home(request):
    return render(request, 'core/home.html')



@login_required
def predicciones_disponibles(request):
    actualizar_fases_automaticamente()

    if not hasattr(request.user, 'perfilusuario') or not request.user.perfilusuario.validado:
        return render(request, 'core/no_validado.html')

    fases = Fase.objects.filter(desbloqueada=True).order_by('orden')
    partidos = Partido.objects.filter(fase__in=fases).order_by('fecha')
    predicciones_hechas = Prediccion.objects.filter(usuario=request.user)

    if request.method == 'POST':
        for partido in partidos:
            clave_local = f"goles_local_{partido.id}"
            clave_visitante = f"goles_visitante_{partido.id}"

            if clave_local in request.POST and clave_visitante in request.POST:
                try:
                    goles_local = int(request.POST[clave_local])
                    goles_visitante = int(request.POST[clave_visitante])
                    prediccion, created = Prediccion.objects.get_or_create(
                        usuario=request.user,
                        partido=partido,
                        defaults={'goles_local': goles_local, 'goles_visitante': goles_visitante}
                    )
                    if not created:
                        messages.warning(request, f"Ya habías predicho {partido}")
                except ValueError:
                    messages.error(request, f"Entrada inválida en el partido {partido}")

        return redirect('predicciones')

    return render(request, 'core/predicciones.html', {
        'partidos': partidos,
        'predicciones': predicciones_hechas
    })


@staff_member_required
def gestion_usuarios(request):
    perfiles = PerfilUsuario.objects.all()

    if request.method == 'POST':
        for perfil in perfiles:
            estado = request.POST.get(f'validado_{perfil.user.id}', 'off') == 'on'
            perfil.validado = estado
            perfil.save()
        messages.success(request, "Cambios guardados.")
        return redirect('gestion_usuarios')

    return render(request, 'core/gestion_usuarios.html', {'perfiles': perfiles})


@login_required
def clasificacion(request):
    usuarios = User.objects.all()
    tabla = []

    for usuario in usuarios:
        predicciones = Prediccion.objects.filter(usuario=usuario)
        total = sum(calcular_puntos(p) for p in predicciones)
        total += puntos_por_bonus(usuario)
        tabla.append((usuario.username, total))

    tabla.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'core/clasificacion.html', {'tabla': tabla})

@login_required
def resultados_en_vivo(request):
    partidos = Partido.objects.order_by('fecha')
    predicciones_usuario = Prediccion.objects.filter(usuario=request.user)
    predicciones_dict = {p.partido.id: p for p in predicciones_usuario}

    resultados = []

    for partido in partidos:
        pred = predicciones_dict.get(partido.id)
        if partido.goles_local is None or partido.goles_visitante is None:
            estado = "Pendiente"
        elif pred is None:
            estado = "Sin predicción"
        elif (pred.goles_local == partido.goles_local and pred.goles_visitante == partido.goles_visitante):
            estado = "✅ Exacto"
        else:
            resultado_real = partido.goles_local - partido.goles_visitante
            resultado_pred = pred.goles_local - pred.goles_visitante

            if (resultado_real > 0 and resultado_pred > 0) or \
               (resultado_real < 0 and resultado_pred < 0) or \
               (resultado_real == 0 and resultado_pred == 0):
                estado = "Correcto"
            else:
                estado = "Incorrecto"

        resultados.append({
            'partido': partido,
            'prediccion': pred,
            'estado': estado
        })

    return render(request, 'core/resultados_en_vivo.html', {'resultados': resultados})
@staff_member_required
def panel_admin(request):
    fases = Fase.objects.order_by('orden')
    partidos = Partido.objects.select_related('fase').order_by('fecha')
    predicciones = Prediccion.objects.select_related('usuario', 'partido')

    data_predicciones = {}
    for pred in predicciones:
        if pred.partido_id not in data_predicciones:
            data_predicciones[pred.partido_id] = []
        data_predicciones[pred.partido_id].append(pred)

    return render(request, 'core/panel_admin.html', {
        'fases': fases,
        'partidos': partidos,
        'predicciones_por_partido': data_predicciones
    })


@login_required
def prediccion_bonus(request):
    try:
        instance = PrediccionBonus.objects.get(usuario=request.user)
    except PrediccionBonus.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = PrediccionBonusForm(request.POST, instance=instance)
        if form.is_valid():
            bonus = form.save(commit=False)
            bonus.usuario = request.user
            bonus.save()
            messages.success(request, "¡Predicción bonus guardada!")
            return redirect('bonus')
    else:
        form = PrediccionBonusForm(instance=instance)

    return render(request, 'core/prediccion_bonus.html', {'form': form})

@staff_member_required
def exportar_ranking_csv(request):
    usuarios = User.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ranking.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Puntos'])

    for usuario in usuarios:
        predicciones = Prediccion.objects.filter(usuario=usuario)
        total = sum(calcular_puntos(p) for p in predicciones)
        total += puntos_por_bonus(usuario)
        writer.writerow([usuario.username, total])

    return response

@staff_member_required
def exportar_predicciones_csv(request):
    predicciones = Prediccion.objects.select_related('usuario', 'partido')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predicciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Partido', 'Predicción', 'Resultado Real'])

    for p in predicciones:
        resultado = f"{p.partido.goles_local}-{p.partido.goles_visitante}" if p.partido.goles_local is not None else "Pendiente"
        writer.writerow([
            p.usuario.username,
            f"{p.partido.equipo_local} vs {p.partido.equipo_visitante}",
            f"{p.goles_local}-{p.goles_visitante}",
            resultado
        ])

    return response