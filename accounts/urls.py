from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from accounts.forms import MyAuthForm
app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=MyAuthForm), name='login'),
    path('edit/', views.Edit.as_view(), name="edit_account"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name="signup"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
