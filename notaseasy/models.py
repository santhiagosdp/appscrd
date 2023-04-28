from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class NotaFiscal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='notas_fiscais/')

    def __str__(self):
        return self.titulo

