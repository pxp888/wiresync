from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.welcome),
    path('test', views.test, name='test'),
    path('account/', views.account, name='account'),
]


