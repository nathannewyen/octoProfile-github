from django.urls import path
from . import views
from .views import ChartData

urlpatterns = [
    path('', views.index),
    path('search', views.searchUser),
    path('<username>', views.user),
    path('403/', views.permission_denied_view),
    path('api/chart/data/', ChartData.as_view(), name='api-data'),
]
