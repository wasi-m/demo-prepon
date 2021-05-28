from django.urls import path

from . import views

app_name = 'fileupload'

urlpatterns = [
    path('', views.index, name='index'),
]