from django.db.models import Manager
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if "mobile" not in extra_fields:
            raise ValueError('شماره موبایل الزامی است')
        return super().create_user(username, email, password, **extra_fields)

    def get_user_by_mobile(self, mobile):
        return self.get(mobile=mobile)

