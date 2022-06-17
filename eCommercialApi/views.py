import stripe as stripe
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .models import Category, Product, ProductAttribute, User, Bookmark, BookmarkDetail
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer, ProductDetailSerializer, \
    UserSerializer, BookmarkSerializer, CreateUserSerializer, BookmarkDetailSerializer, BookmarkDetailCreateSerializer

stripe.api_key = 'sk_test_51KAS9GEAPiKpbC1NsDSO98Tt5dPSoe27YloBRwOD8ayF0xCHSjmG8mHeUNSHG5yqUhf735aM2GyRDdvH3KX8SqAs00WUm2YbBa'


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = CreateUserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        context = super().get_serializer_context()
        return Response(UserSerializer(request.user, context=context).data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def create_payment(self, id):
        user = User.objects.filter(id=id)
        first_name = user.values_list('first_name', flat=True).first()
        last_name = user.values_list('last_name', flat=True).first()
        email = user.values_list('email', flat=True).first()
        full_name = first_name + ' ' + last_name
        created_customer = stripe.Customer.create(name=full_name, email=email)
        user.update(stripe_id=created_customer.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.create_payment(serializer.data["id"])
        user = User.objects.get(id=serializer.data["id"])
        b = Bookmark(user=user)
        b.save()

        return Response('Success', status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='product')
    # product/
    def get_product_by_category(self, query, pk):
        context = super().get_serializer_context()
        if int(pk) == 0:
            products = Product.objects.all()
        else:
            category = Category.objects.get(pk=pk)
            products = category.products.all()

        return Response(data=ProductSerializer(products, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    pagination_class = ProductPaginator

    # def get_permissions(self):
    # if self.action == 'list':
    # return [permissions.AllowAny()]

    # return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=True, url_path='productAttributes')
    # product/
    def get_product_attribute(self, query, pk):
        context = super().get_serializer_context()
        product = Product.objects.get(pk=pk)
        product_attributes = product.productAttribute.all()

        return Response(data=ProductAttributeSerializer(product_attributes, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class BookmarkViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Bookmark.objects
    serializer_class = BookmarkSerializer

    @action(methods=['get'], detail=False, url_path='getBookmarkByUser')
    # product/
    def get_bookmark_by_user(self, query):
        context = super().get_serializer_context()
        user = self.request.user
        bookmark = self.queryset.filter(user=user).first()
        print(bookmark)
        return Response(data=BookmarkSerializer(bookmark, many=False, context=context).data,
                        status=status.HTTP_200_OK)


class BookmarkDetailViewSet(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = Bookmark.objects
    serializer_class = BookmarkDetailCreateSerializer

    @action(methods=['delete'], detail=False, url_path='deleteBookmark/(?P<my_pk>[^/.]+)')
    # product/
    def delete_bookmark(self, query, my_pk=None):
        print(my_pk)
        instance = BookmarkDetail.objects.filter(id=my_pk)
        instance.delete()
        user = self.request.user
        bookmark = self.queryset.filter(user=user).first()
        context = super().get_serializer_context()
        return Response(data=BookmarkSerializer(bookmark, many=False, context=context).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="addBookmark")
    def add_bookmark(self, query):
        productAttributeId = self.request.data['productAttribute']
        bookmarkId = self.request.data['bookmark']
        BookmarkDetail.objects.update_or_create(productAttribute_id=productAttributeId, bookmark_id=bookmarkId)
        user = self.request.user
        bookmark = self.queryset.filter(user=user).first()
        context = super().get_serializer_context()
        return Response(data=BookmarkSerializer(bookmark, many=False, context=context).data,
                        status=status.HTTP_200_OK)


class ProductAttributeViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ProductAttribute.objects.filter(active=True)
    serializer_class = ProductAttributeSerializer


@api_view(['GET'])
def get_stripe_costumer(request):
    customer_stripe = stripe.Customer.retrieve(request.user.stripe_id)
    return Response(status=status.HTTP_200_OK, data=customer_stripe)


@api_view(['GET'])
def get_all_payment(request):
    payment_method = stripe.Customer.list_sources(request.user.stripe_id, object="card")
    return Response(status=status.HTTP_200_OK, data=payment_method)


@api_view(['POST'])
def post_new_payment(request):
    card = request.data["cardDetail"]
    print(card["number"])
    card_token = stripe.Token.create(
        card={
            "number": card["number"],
            "name": card["fullName"],
            "exp_month": card["exp_month"],
            "exp_year": card["exp_year"],
            "cvc": card["cvc"],
            "currency": "vnd",
        },
    )
    new_card = stripe.Customer.create_source(
        request.user.stripe_id,
        source=card_token.id
    )
    response = stripe.PaymentMethod.attach(new_card.id, customer=request.user.stripe_id)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_default_payment(request):
    response = stripe.Customer.modify(
        request.user.stripe_id,
        invoice_settings={
            'default_payment_method': request.data["card_id"]
        },
    )
    return Response(response, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def detach_payment_method(request):
    response = stripe.Customer.delete_source(
        request.user.stripe_id,
        request.data["card_id"]
    )
    return Response(response, status=status.HTTP_200_OK)


def index(request):
    return render(request, template_name='index.html', context={
        "name": 'Long Phú'
    })
