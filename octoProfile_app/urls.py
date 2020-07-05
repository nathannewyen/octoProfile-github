from django.urls import path
from . import views
from django.conf.urls import handler403, handler404, handler500

urlpatterns = [
    path('', views.index),
    path('search', views.searchUser),
    path('<username>', views.user),
]


handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.server_error
