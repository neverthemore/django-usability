from django.urls import path

from . import views


app_name = "dialog_bot"
urlpatterns = [
    path("", views.index, name="index"),
    path("clear/", views.clear, name="clear"),
]

