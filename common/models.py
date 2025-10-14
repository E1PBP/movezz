"""
Ini adalah file untuk menyimpan model-model umum yang digunakan di berbagai aplikasi dalam proyek ini.
Jika ingin menggunakan model di aplikasi lain, cukup impor model ini dari aplikasi common.
"""

from django.db import models

class Sport(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Badge(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=80)
    icon_url = models.CharField(max_length=255, blank=True, null=True) # ini nanti insert manual aja di django admin pake link. ga usah pake cloudinary

    def __str__(self):
        return self.name

class Hashtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag
