from django.db import models

# Create your models here.


class Pokemon(models.Model):
    imagen = models.URLField()
    nombre = models.CharField(max_length=100)
    estadisticas = models.JSONField(default=dict)
    tipo1 = models.CharField(max_length=30)
    tipo2 = models.CharField(max_length=30, blank=True, null=True)
    habilidad = models.CharField(max_length=100)
    evolucion = models.CharField(max_length=100, blank=True, null=True)
    legendario = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Entrenador(models.Model):
    img = models.URLField(blank=True, null=True)
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    medallas = models.IntegerField(default=0)
    liga = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    pueblo = models.CharField(max_length=50)
    profesor_asignado = models.CharField(max_length=100)
    pokemon = models.ManyToManyField(Pokemon, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Gym(models.Model):
    lider_gimnasio = models.CharField(max_length=50)
    tipo_elemento = models.CharField(max_length=30)
    medalla = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    region = models.CharField(max_length=50)

    def __str__(self):
        return self.lider_gimnasio


class Backup(models.Model):
    entrenador = models.ForeignKey(Entrenador,on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE)
    profesor = models.CharField(max_length=100)
    items = models.JSONField(default=list, blank=True)
    region = models.CharField(max_length=50)

    def __str__(self):
        return f"Backup de {self.entrenador}"
