from django.contrib import admin
from django.urls import path
from pagweb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('product/', views.product, name='product'),
    path('event/', views.event, name='event'),
    path('request/', views.request, name='request'),
    path('information/', views.information, name='information'),
    path('version/', views.version, name='version'),
]
