from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()), 
    path('products/<str:slug>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view(), name='collections'), 
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'), 
]
