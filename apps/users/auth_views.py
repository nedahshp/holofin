from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import View, FormView, TemplateView
from .auth_forms import LoginPasswordForm, MobileForm, RegisterForm
User = get_user_model()

class RegisterView(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('auth:login')
    template_name = 'gentellela/register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SuccessRegisterView(TemplateView):
    template_name = 'gentellela/register_succeed.html'


class LogoutView(View):
    def get(self, request, *args: str, **kwargs):
        logout(request)
        return redirect(reverse('users:dashboard'))

