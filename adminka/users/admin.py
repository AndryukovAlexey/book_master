from django.contrib import admin
from .models import Users, Books

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')

@admin.register(Books)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
