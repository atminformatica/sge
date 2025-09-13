from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view() , name='login'),
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),

    path('',views.home,name='home'),

    path('', include('brands.urls')),
    path('categories/', include('categories.urls')),
    path('supplier/', include('suppliers.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path('', include('products.urls')),
    path('', include('bulletins.urls')),
]
