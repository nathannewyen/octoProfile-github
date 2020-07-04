from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('search', views.searchUser),
    path('<username>', views.user),
]
