from secrets import choice
from django import forms
from django_filters import FilterSet
from django.contrib.auth import get_user_model
from apps.core import utils
User = get_user_model()


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password= forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'role', 'avatar', 'password', 'password_confirm']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if password.isdigit():
            raise forms.ValidationError('رمز عبور نمیتواند تنها شامل عدد باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password:
            return password_confirm
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن باید یکسان باشد')
        return password_confirm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'role', 'avatar']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.choices = UserForm.remove_patient_from_roles(User.Roles.choices)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
 
        
class UserSetPasswordForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password= forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


    class Meta:
        model = User
        fields = ['password', 'password_confirm']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if password.isdigit():
            raise forms.ValidationError('رمز عبور نمیتواند تنها شامل عدد باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password:
            return password_confirm
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن باید یکسان باشد')
        return password_confirm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'national_code',
                  'email', 'address', 'avatar', 'deposit_quantity')
         

