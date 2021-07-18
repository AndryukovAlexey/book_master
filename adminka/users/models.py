
from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    photo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'books'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0, null=True)
    ref_link = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'
