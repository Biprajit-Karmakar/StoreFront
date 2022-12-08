from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()), 
    path('products/<str:slug>/', views.ProductDetail.as_view()),
    path('collections/', views.collection_list, name='collections'), 
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail'), 
]
