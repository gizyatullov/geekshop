from django.urls import path

from authnapp.apps import AuthnappConfig
import authnapp.views as authnapp

app_name = AuthnappConfig.name

urlpatterns = [
    path('login/', authnapp.login, name='login'),
    path('logout/', authnapp.logout, name='logout'),
    path('register/', authnapp.register, name='register'),
    path('edit/', authnapp.edit, name='edit'),
]
