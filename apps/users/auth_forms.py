from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from apps.core import utils
from apps.institution.models import Institution
from .models import User
User = get_user_model()


class MobileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('mobile', )

    def validate_unique(self):
        return


class LoginPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('mobile', 'password', )
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['mobile'].widget = forms.HiddenInput()
        self.error_messages = {
            'invalid_login': 'رمز وارد شده صحیح نمی‌باشد',
            'inactive': 'حساب شما مسدود شده است. جهت رفع مسدودی حساب با پشتیبانی تماس بگیرید.',
        }
        self._user = None

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('رمز عبور الزامی است')
        return password

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')

        if mobile is not None and password:
            __user = User.objects.get_user_by_mobile(mobile)
            __user = authenticate(self.request, username=__user.username, password=password)
            if __user is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(__user)
            self._user = __user

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'mobile': 'موبایل'},
        )

    def get_user(self):
        return self._user


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='رمز ورود',
                               required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput,
                                       label='تکرار رمز ورود', required=True)
    institution_name = forms.CharField(label='نام موسسه', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', 'password', 'password_confirm', 'institution_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = 'chrome-off'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('رمز عبور الزامی است')
        if len(password) < 6:
            raise forms.ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور با تکرار آن یکسان نیست')
        return password_confirm

        
    def save(self, commit=True):
        user = super().save(commit=False)
        institution_name = self.cleaned_data.get('institution_name')
        institution = Institution.objects.create(name=institution_name)
        user.mobile = self.cleaned_data.get('mobile')
        user.username = user.mobile
        user.institution = institution
        user.role = User.Roles.ADMIN
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        su = super()
        if hasattr(su, 'clean_username'):
            su.clean_username()
        username = self.cleaned_data["username"]
        username = utils.persian_digits_to_english(username)
        return username

