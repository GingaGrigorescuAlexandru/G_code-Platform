from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'email')
    list_display = ('id', 'username', 'email')

# Register your models here.
