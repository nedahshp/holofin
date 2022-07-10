from django.urls import path
from apps.users.auth_views import RegisterView, LogoutView, SuccessRegisterView
from django.contrib.auth import views as auth_views


app_name = 'auth'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='gentellela/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/complete/', SuccessRegisterView.as_view(), name='register_succeed'),
]
