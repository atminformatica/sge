from django.urls import path
from . import views

urlpatterns = [
    path('bulletins/create/', views.criar_boletim, name='criar_boletim'),
]