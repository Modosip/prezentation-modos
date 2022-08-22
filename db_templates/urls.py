from django.urls import path

from . import views

urlpatterns = [
    path('', views.dbtemplates, name='dbtemp'),
]