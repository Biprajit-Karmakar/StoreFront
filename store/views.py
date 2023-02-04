from django.db.models import Count
from  django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermisssion

from . models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes= [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    # no changes for create and update but have to overright the logic to delete 
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error': 'Prouduct Can not be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    # set product filter in queryset so overright the get_queryset
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
        # our url has two parameter pk & product_pk


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    # no changes for create and update but have to overright the logic to delete 
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(Collection_id = kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
        return super().destroy(request, *args, **kwargs)



class CartViewSet(CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    # queryset = Cart.objects.all()
    # to avoid similar or duplicate queries we should wright in prefetch_releted mode for multiple items and select-related for single items
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):    
    # serializer_class = CartItemSerializer
    # we return dynamical serializer_class depending on the request method
    http_method_names = ['get','post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')




class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @action(detail=True, permission_classes= [ViewCustomerHistoryPermisssion])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':            
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id = user.id)
        return Order.objects.filter(customer_id=customer_id)





















# class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [IsAuthenticated]

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     @action(detail=False, methods=['GET', 'PUT'])
#     def me(self, request):
#         (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
#         if request.method == 'GET':            
#             serializer = CustomerSerializer(customer)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = CustomerSerializer(customer, data= request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('Collection').all()
#         serializer = ProductSerializer(queryset, many= True, context={'request':request})
#         return Response(serializer.data)
#     def post(self, request):
#         serializer =ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



    # GENERIC VIEW 
    # queryset = Product.objects.select_related('Collection').all()
    # serializer_class = ProductSerializer


# class ProductDetail(APIView):    
#     def get(self, request, slug):
#         product = get_object_or_404(Product,slug=slug)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)  
    
#     def put(self, request, slug):
#         product = get_object_or_404(Product,slug=slug)
#         serializer = ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, slug):
#         product = get_object_or_404(Product,slug=slug)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Prouduct Can not be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    # GENERICVIEW -
    # RetrieveUpdateAPIView
    # no changes for create and update but have to overright the logic to delete 
    
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # def delete(self, request, slug):
    #     product = get_object_or_404(Product,slug=slug)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Prouduct Can not be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):

#     # APIView
#     # def get(self, request):
#     #     queryset = Collection.objects.annotate(products_count = Count('products')).all()
#     #     serializer = CollectionSerializer(queryset, many= True)
#     #     return Response(serializer.data)
#     # def post(self, request):
#     #     serializer =CollectionSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # generic view
#     queryset = Collection.objects.annotate(products_count = Count('products')).all()
#     serializer_class = CollectionSerializer


