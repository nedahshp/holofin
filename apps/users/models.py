from time import perf_counter
from django.templatetags.static import static
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from apps.core.models import AbstractModel
from apps.institution.models import Institution
from .validators import MobileValidator, NationalCodeValidator
from .managers import CustomUserManager



class User(AbstractUser, AbstractModel):
    """Custom User model"""
    class DeactivateReasons(models.IntegerChoices):
        UNKNOWN = 0, 'نامشخص'
        BY_ADMIN = 1, 'غیر فعال توسط مدیر'
        VERIFY_MOBILE = 2, 'عدم تایید موبایل'
        VERIFY_EMAIL = 3, 'عدم تایید ایمیل'
    
    class Roles(models.IntegerChoices):
        ADMIN = 0, 'مدیر'
        USER = 1, 'کاربر'

    mobile = models.CharField('موبایل', max_length=11, unique=True,
                              help_text='موبایل باید به فرمت 09123456789 وارد شود',
                              validators=[MobileValidator()],
                              error_messages={
                                  'unique': 'این شماره موبایل از قبل در سامانه ثبت شده است',
                                },
                            )
    password = models.CharField('گذرواژه', max_length=128, null=True, blank=True)
    first_name = models.CharField(verbose_name='نام', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150, blank=True)
    national_code = models.CharField(max_length=10, verbose_name='کد ملی',
                                     validators=[NationalCodeValidator()],
                                     null=True, blank=True, unique=True)
    deactivate_reason = models.PositiveSmallIntegerField(choices=DeactivateReasons.choices,
                                                         default=DeactivateReasons.UNKNOWN,
                                                         verbose_name='غیرفعال به دلیل')
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='ایمیل')
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    birth_date = models.DateField(verbose_name='تاریخ تولد', null=True, blank=True)
    role = models.IntegerField(choices=Roles.choices, default=Roles.USER, verbose_name='نقش')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تلفن ثابت', null=True, blank=True)
    notes = models.TextField(verbose_name='یادداشت', null=True, blank=True)
    avatar = models.ImageField(verbose_name='تصویر پروفایل', upload_to='users/avatars', null=True, blank=True)
    deposit_quantity = models.PositiveIntegerField(verbose_name='تعداد سهم', default=1)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, related_name='users')
    objects = CustomUserManager()

    REQUIRED_FIELDS = ["mobile", ]

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'
        ordering = ('-id',)

    def __str__(self):
        role = self.get_role_display()
        return f'{self.display_name} ({role})'

    def get_absolute_url(self):
        return reverse('users:user_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.email == '':
            self.email = None
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def display_name(self) -> str:
        return (
            self.first_name + ' ' + self.last_name
            if self.first_name and self.last_name
            else self.mobile
        )

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        f = static('account/profile.png')
        return f

    def deactivate(self, reason: DeactivateReasons):
        """Deactivate user by reason

        DO NOT explicitly set users is_active field without saving the reason why it is deactivated
        """
        self.deactivate_reason = reason
        self.is_active = False
        self.save()

    def activate(self):
        """Activate user

        Will change user's deactivate reason to UNKNOWN
        """
        self.deactivate_reason = self.DeactivateReasons.UNKNOWN
        self.is_active = True
        self.save()

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_simple_user(self):
        return self.role == self.Roles.USER
