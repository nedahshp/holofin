from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView, CreateView, UpdateView, TemplateView, FormView
from jalali_date import date2jalali, datetime2jalali
from apps.core.permissions import PermissionRequireMixin, Permissions
from apps.core.base import BaseContextMixin, GenericFormView, GenericModelFormView
from apps.core.mixins import CustomFormTemplateMixin, CustomListTemplateMixin
from .forms import UserForm, UserProfileForm, UserUpdateForm, UserSetPasswordForm
User = get_user_model()


class DashboardView(LoginRequiredMixin, BaseContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'users/dashboard.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileUpdateView(LoginRequiredMixin, CustomFormTemplateMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:dashboard')
    success_message = 'اطلاعات شما با موفقیت بروزرسانی شد.'
    page_title = 'ویرایش پروفایل'

    def get_page_subtitle(self):
        user = self.request.user
        return user.get_full_name()

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_scripts'] = ['users/scripts/career_dropdown.js']
        return context

        
class UserListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions =  [User.Roles.ADMIN, ]
    page_title = 'لیست کاربران'
    context_object_name = 'users'
    paginate_by = 100
    ordering = '-created_at'
    fields = ['username', 'first_name', 'last_name', 'role',]
    header_buttons = [{'title': 'افزودن کاربر', 'url': reverse_lazy('users:new_user')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'users:update_user', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
        {'title': 'تغییر رمز', 'url_name': 'users:set_password', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': 'btn-warning', 'class_form_field': 'id'},
    ]

    def get_queryset(self):
        institution = self.request.user.institution
        return User.objects.filter(institution=institution)

    def get_role(self, obj):
        return obj.get_role_display()

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')

    def get_last_login(self, obj):
        last_login = obj.last_login
        if last_login:
            return datetime2jalali(last_login).strftime('%Y/%m/%d %H:%M:%S')
        return '-'


class UserCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.ADMIN]
    model = User
    form_class = UserForm
    page_title = 'افزودن کاربر جدید'
    success_url = reverse_lazy('users:user_list')
    cancel_url = reverse_lazy('users:user_list')
    success_message = ' کاربر جدید با موفقیت ثبت شد.'

    def form_valid(self, form):
        user = form.save(commit=False)
        password = user.password
        user.username = user.mobile
        user.institution = self.request.user.institution
        user.set_password(password)
        user.save()
        return super().form_valid(form)



class UserUpdateView(UserCreateView, UpdateView):
    page_title = 'ویرایش کاربر'
    success_message = 'کاربر با موفقیت ویرایش شد.'
    form_class = UserUpdateForm


class UserSetPasswordView(CustomFormTemplateMixin, PermissionRequireMixin, FormView):
    permissions = [User.Roles.ADMIN]
    model = User
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('users:user_list')
    success_message = 'رمز عبور با موفقیت بروزرسانی شد.'
    page_title = 'تغییر رمز عبور'
    
    def get_page_subtitle(self):
        user = self.get_object()
        return user.get_full_name()

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)
    
    def form_valid(self, form):
        user = self.get_object()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class UserDetailView(PermissionRequireMixin ,TemplateView):
    permissions = [User.Roles.ADMIN]
    template_name = 'users/user_detail_view.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=kwargs['pk'])
        context["user"] = user
        return context

