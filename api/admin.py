from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'username',
        'email',
        'confirme_code',
        'bio',
        'role'
    )
    list_filter = ('username',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
