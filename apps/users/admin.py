from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(User)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    list_display = ('mobile', 'username', 'first_name', 'last_name', 'is_staff', 'email')
    search_fields = ('mobile', 'username', 'first_name', 'last_name', 'email', 'notes')
    fieldsets = (
        (None, {'fields': ('mobile', 'username', 'password')}),
        ('اطلاعات فردی', {'fields': ('first_name', 'last_name', 'email', 'notes',
                                     'national_code', 'birth_date',
                                     'address', 'phone_number')}),
        ('دسترسی‌ها', {'fields': ('role',)}),
        ("تاریخ‌های مهم", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'mobile', 'username', 'role', 'national_code',
                       'address', 'birth_date', 'phone_number', 'notes'
                      )}
         ),
    )
