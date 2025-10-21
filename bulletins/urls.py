from django.urls import path
from . import views

urlpatterns = [
    # path('bulletins/create/', views.criar_boletim, name='criar_boletim'),
    path('bulletins/create/', views.BulletinCreateView.as_view(), name='criar_boletim'),

    path('bulletins/list/', views.BulletinListView.as_view(), name='bulletin_list'),
    path('bulletins/<int:pk>/detail/', views.BulletinDetailView.as_view(), name='bulletin_detail'),
    
    path('boletim/<int:pk>/pdf/', views.BulletinPDFView.as_view(), name='bulletin_pdf'),

    path('bulletins/<int:pk>/update/', views.BulletinUpdateView.as_view(), name='bulletin_update'),
    path('bulletins/<int:pk>/delete/', views.BulletinDeleteView.as_view(), name='bulletin_delete'),

    path('buscar-envolvido/', views.buscar_envolvido_por_cpf, name='buscar_envolvido'),
]