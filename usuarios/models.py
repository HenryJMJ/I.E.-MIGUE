from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
import string
import random
from datetime import timedelta

User = get_user_model()

def generate_code():
    return ''.join(random.choices(string.digits, k=6))


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)  # Código de 6 dígitos
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def is_valid(self):
        tiempo_expiracion = timedelta(minutes=10)
        return not self.is_used and timezone.now() - self.created_at <= tiempo_expiracion

    def __str__(self):
        return f"{self.user.username} - {self.code}"

class Perfil(models.Model):
    ROLES = (
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
class Acceso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('info', 'Información'),
        ('advertencia', 'Advertencia'),
        ('mensaje', 'Mensaje'),
    ]

    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='info')
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificaciones_creadas')
    usuario_afectado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificaciones_recibidas')
    eliminada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"
    
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos')  # Relación con el usuario/docente
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Recurso(models.Model):
    archivo = models.FileField(upload_to='recursos/')  # Archivos se guardan en media/recursos/
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion
