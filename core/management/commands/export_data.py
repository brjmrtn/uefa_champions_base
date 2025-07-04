from django.core.management.base import BaseCommand
import pandas as pd
import os
from core.models import Partido, Prediccion, PrediccionBonus

class Command(BaseCommand):
    help = "Exporta tablas clave a Parquet/csv para Spark"

    def handle(self, *args, **options):
        #hay que asegurarse que la carpeta data/ existe
        os.makedirs('data', exist_ok=True)

        # 1) Exportar partidos
        qs = Partido.objects.all().values(
            'id', 'fase_id', 'equipo_local', 'equipo_visitante', 'fecha','goles_local', 'goles_visitante'
        )
        df_partidos = pd.DataFrame.from_records(qs)
        df_partidos.to_parquet('data/partidos.parquet', index=False)
        self.stdout.write(self.style.SUCCESS("✔ partidos.parquet creado"))

        # 2) Exportar predicciones
        qs = Prediccion.objects.all().values(
            'id', 'usuario_id', 'partido_id', 'goles_local', 'goles_visitante', 'fecha_prediccion'
        )
        df_pred= pd.DataFrame.from_records(qs)
        df_pred.to_parquet('data/predicciones.parquet', index=False)
        self.stdout.write(self.style.SUCCESS('✔ predicciones.parquet creado'))

        # 3) Exportar bonus (opcional)
        qs = PrediccionBonus.objects.all().values(
            'usuario_id', 'campeon', 'goleador', 'mvp'
        )
        df_bonus = pd.DataFrame.from_records(qs)
        df_bonus.to_parquet('data/bonus.parquet', index=False)
        self.stdout.write(self.style.SUCCESS('✔ bonus.parquet creado'))
