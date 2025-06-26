from .models import Fase, Partido, PrediccionBonus

def actualizar_fases_automaticamente():
    fases = Fase.objects.order_by('orden')

    for i in range(len(fases) - 1):
        fase_actual = fases[i]
        fase_siguiente = fases[i + 1]

        if fase_actual.desbloqueada and not fase_siguiente.desbloqueada:
            partidos = Partido.objects.filter(fase=fase_actual)
            todos_finalizados = all(p.goles_local is not None and p.goles_visitante is not None for p in partidos)

            if todos_finalizados:
                fase_siguiente.desbloqueada = True
                fase_siguiente.save()

def calcular_puntos(prediccion):
    partido = prediccion.partido
    if partido.goles_local is None or partido.goles_visitante is None:
        return 0  # partido no finalizado

    if (prediccion.goles_local == partido.goles_local and
        prediccion.goles_visitante == partido.goles_visitante):
        return 3  # resultado exacto

    resultado_real = partido.goles_local - partido.goles_visitante
    resultado_pred = prediccion.goles_local - prediccion.goles_visitante

    if (resultado_real > 0 and resultado_pred > 0) or \
       (resultado_real < 0 and resultado_pred < 0) or \
       (resultado_real == 0 and resultado_pred == 0):
        return 1  # signo correcto

    return 0

def obtener_campeon_real():
    try:
        final = Partido.objects.get(fase__nombre__iexact='Final')
        if final.goles_local is None or final.goles_visitante is None:
            return None
        if final.goles_local > final.goles_visitante:
            return final.equipo_local
        elif final.goles_visitante > final.goles_local:
            return final.equipo_visitante
        else:
            return "Empate"
    except Partido.DoesNotExist:
        return None

def puntos_por_bonus(usuario):
    try:
        bonus = usuario.prediccionbonus
        campeon_real = obtener_campeon_real()
        if campeon_real is None:
            return 0
        return 5 if bonus.campeon.lower() == campeon_real.lower() else 0
    except:
        return 0