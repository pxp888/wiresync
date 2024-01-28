from . import views, account, welcome
from django.urls import path

urlpatterns = [
    path('', welcome.welcome),
    path('home/', views.home, name='home'),
    path('account/', account.account, name='account'),
    path('logout/', welcome.logout, name='logout'),
    path('test', views.test, name='test'),
]

