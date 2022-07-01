from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='dashboard-index'),
    path('inventory/', views.index, name='dashboard-index'),
    path('scan/', views.scan, name='dashboard-scan'),
    path('borrowed/', views.borrowed, name='dashboard-borrowed'),
    path('inventory/<str:item_PN>/', views.detail, name='dashboard-detail'),
]
