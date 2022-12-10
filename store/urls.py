from django.urls import include, path
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

prouducts_router = routers.NestedDefaultRouter(router,'products', lookup='product')
prouducts_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
urlpatterns = [
    # add router to urls 
    path('', include(router.urls)),
    path('', include(prouducts_router.urls)),

    # path('products/', views.ProductList.as_view()), 
    # path('products/<str:slug>/', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view(), name='collections'), 
    # path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'), 
]
