from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class Permissions:
    ADMIN = 'admin'
    USER = 'user'

class PermissionRequireMixin:
    permissions = [Permissions.USER]

    def get(self, *args, **kwargs):
        if not self.has_permission():
            return self.redirect_to_login()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.has_permission():
            return self.redirect_to_login()
        return super().post(*args, **kwargs)
            
    def has_permission(self):
        if not self.permissions:
            return True
        user = self.request.user
        if self.request.user.is_superuser:
            return True
        if not user.is_authenticated:
            return False
        if user.role not in self.permissions:
            return False
        return True
   

    def redirect_to_login(self):
        messages.error(self.request, 'شما به این صفحه دسترسی ندارید. در صورت نیاز با نام کاربری دیگری وارد شوید')
        url = reverse_lazy(settings.LOGIN_URL) + '?next=' + self.request.path
        return redirect(url)
        
        
            

        