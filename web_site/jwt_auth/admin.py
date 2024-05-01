from django.contrib import admin
from .models import User, RefreshToken


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('is_active', 'is_staff')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):

    list_display = ('user', 'token', 'expiration_date')
    list_filter = ('user',)
    search_fields = ('user',)
    readonly_fields = ('user', 'token', 'expiration_date')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
