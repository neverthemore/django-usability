from django.urls import path

from . import views


app_name = "image_classifier"
urlpatterns = [path("", views.index, name="index")]

