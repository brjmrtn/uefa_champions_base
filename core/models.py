from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Fase(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    desbloqueada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.orden}. {self.nombre}"

class Partido(models.Model):
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    equipo_local = models.CharField(max_length=50)
    equipo_visitante = models.CharField(max_length=50)
    fecha = models.DateTimeField()
    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} ({self.fase})"

    def esta_finalizado(self):
        return self.goles_local is not None and self.goles_visitante is not None

class Prediccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    goles_local = models.IntegerField()
    goles_visitante = models.IntegerField()
    fecha_prediccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'partido')

    def __str__(self):
        return f"{self.usuario.username} → {self.partido}: {self.goles_local}-{self.goles_visitante}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} (validado: {self.validado})"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

class PrediccionBonus(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    campeon = models.CharField(max_length=50)
    goleador = models.CharField(max_length=50)
    mvp = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.usuario.username} (bonus)"
