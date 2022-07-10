from django.urls import include, path
from apps.users.views import (
    DashboardView, ProfileUpdateView, UserListView, UserUpdateView,
    UserCreateView, UserSetPasswordView
)


app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='new_user'),
    path('<pk>/set-password/', UserSetPasswordView.as_view(), name='set_password'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', DashboardView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('<pk>/update/', UserUpdateView.as_view(), name='update_user'),
]
