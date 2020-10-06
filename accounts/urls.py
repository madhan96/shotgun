from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.index, name="index1"),
    path("login", views.Login, name="login"),
    path("loginsimple/", views.loginsimple, name="loginsimple"),
    path("logout", views.logout_view, name="logout"),
    path("IT", views.dashboardIT, name="index2"),
    path("upload", views.formupload, name="upload"),
    path("json", views.getdata, name="json_simple"),
]
