from django.utils import timezone
import stripe as stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import json

from .models import Category, Product, ProductAttribute, User, Bookmark, BookmarkDetail, ShippingContact, OrderDetail, \
    Order, ShippingUnit, ShippingType, Payment
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer, ProductDetailSerializer, \
    UserSerializer, BookmarkSerializer, CreateUserSerializer, OrderSerializer, BookmarkDetailCreateSerializer, \
    ShippingContactSerializer, OrderDetailSerializer, ShippingUnitSerializer, ShippingTypeSerializer

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


class ShippingContactViewSet(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = ShippingContact.objects
    serializer_class = ShippingContactSerializer

    @action(methods=['post'], detail=False, url_path="addShippingContact")
    def add_shipping_contact(self, query):
        shippingContact = self.request.data["shippingContact"]
        default = self.request.data["default"]
        savedShippingContact = ShippingContact.objects.create(address=shippingContact["address"],
                                                              district=shippingContact["district"],
                                                              name=shippingContact["name"],
                                                              province=shippingContact["province"],
                                                              telephone=shippingContact["telephone"],
                                                              ward=shippingContact["ward"],
                                                              user=self.request.user
                                                              )

        if default:
            current_user = self.request.user
            current_user.default_address = savedShippingContact.id
            current_user.save()

        return Response(data=savedShippingContact.id,
                        status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False, url_path="updateShippingContact/(?P<my_pk>[^/.]+)")
    def update_shipping_contact(self, request, my_pk=None):
        shippingContact = json.dumps(self.request.data)
        print(shippingContact)
        return Response(data='shippingContact',
                        status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='deleteShippingContact/(?P<my_pk>[^/.]+)')
    def delete_shipping_contact(self, query, my_pk=None):
        user = self.request.user
        instance = ShippingContact.objects.filter(id=my_pk, user=user)
        instance.delete()
        shipping_contact = self.queryset.filter(user=user)
        context = super().get_serializer_context()
        return Response(data=ShippingContactSerializer(shipping_contact, many=True, context=context).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="getAllShippingContact")
    def get_shipping_contact(self, query):
        shipping_contacts = ShippingContact.objects.filter(user=self.request.user)
        context = super().get_serializer_context()
        return Response(data=ShippingContactSerializer(shipping_contacts, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class ProductAttributeViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ProductAttribute.objects.filter(active=True)
    serializer_class = ProductAttributeSerializer


class OrderDetailView(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer
    permission_classes = IsAuthenticated,

    @action(methods=['get'], detail=False, url_path="getCart")
    def get_cart(self, query):
        print('abc')
        try:
            context = super().get_serializer_context()
            order = Order.objects.filter(user=self.request.user, ordered=False).first()
            return Response(OrderSerializer(order, many=False, context=context).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            order = Order()
            order.save()
            return Response(OrderSerializer(order, many=False, context=context).data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path="deleteToCart/(?P<my_pk>[^/.]+)")
    def delete_to_cart(self, query, my_pk=None):
        order_detail_qs = OrderDetail.objects.filter(
            id=my_pk,
            user=self.request.user,
            ordered=False
        )
        if order_detail_qs.exists():
            order_detail = order_detail_qs.first()
            order_detail.delete()
            order_total = Order.objects.filter(user=self.request.user, ordered=False).first().get_total()
            return Response(data=order_total, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="setPayment")
    def set_payment(self, query):
        user = self.request.user
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = super().get_serializer_context()
        shipping_contact = ShippingContact.objects.get(user=user, id=self.request.user.default_address)
        customer_stripe = stripe.Customer.retrieve(self.request.user.stripe_id)
        stripePaymentIntent = stripe.PaymentIntent.create(
            amount=int(order.get_total()),
            payment_method=customer_stripe.default_source,
            currency="usd",
            customer=customer_stripe,
            confirm=True,
            payment_method_types=["card"],
        )

        payment = Payment()
        payment.stripe_charge_id = stripePaymentIntent['id']
        payment.user = self.request.user
        payment.amount = order.get_total()
        payment.save()

        order_details = order.order_details.all()
        order_details.update(ordered=True)
        for order_detail in order_details:
            order_detail.save()

        order.ordered = True
        order.payment = payment
        order.shipping_contact = shipping_contact
        order.save()

        return Response("success",
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="addToCart")
    def add_to_cart(self, query):
        order_detail_qs = OrderDetail.objects.filter(
            product_attribute_id=self.request.data["productAttribute"],
            user=self.request.user,
            ordered=False
        )

        if order_detail_qs.exists():
            order_detail = order_detail_qs.first()
            order_detail.quantity += int(self.request.data["quantity"])
            print(order_detail.quantity)
            if order_detail.quantity > 12:
                return Response(data="the quantity must not over than 12", status=status.HTTP_404_NOT_FOUND)

            order_detail.save()

        else:
            order_detail = OrderDetail.objects.create(
                product_attribute_id=self.request.data["productAttribute"],
                user=self.request.user,
                ordered=False,
                quantity=int(self.request.data["quantity"])
            )
            order_detail.save()

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.order_details.filter(id=order_detail.id).exists():
                order.order_details.add(order_detail)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=self.request.user, ordered_date=ordered_date)
            order.order_details.add(order_detail)

        context = super().get_serializer_context()
        return Response(OrderSerializer(order, many=False, context=context).data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False, url_path="updateQuantity/(?P<my_pk>[^/.]+)")
    def update_quantity(self, query, my_pk=None):
        order_detail = OrderDetail.objects.filter(id=my_pk).first()
        order_detail.quantity = int(self.request.data["quantity"])
        order_detail.save()
        context = super().get_serializer_context()
        order_total = Order.objects.filter(user=self.request.user, ordered=False).first().get_total()
        total_price_item = order_detail.get_total_item_price()
        return JsonResponse({"total_price_item": total_price_item, "order_total": order_total})


class ShippingUnitView(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = ShippingUnit.objects
    serializer_class = ShippingUnitSerializer

    @action(methods=['get'], detail=False, url_path="")
    def get_shipping_unit(self):
        try:
            context = super().get_serializer_context()
            shipping_units = self.queryset.all()
            return Response(self.serializer_class(shipping_units, many=True, context=context).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404("Don't have any shipping unit")


class ShippingTypeView(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = ShippingType.objects
    serializer_class = ShippingTypeSerializer

    @action(methods=['get'], detail=False, url_path="")
    def get_shipping_type(self):
        try:
            context = super().get_serializer_context()
            shipping_types = self.queryset.filter(
                shippingType__shipping_contact_id__in=self.request.data["shipping_unit_id"])
            return Response(self.serializer_class(shipping_types, many=True, context=context).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404("Don't have any shipping unit")


@api_view(['GET'])
def get_stripe_costumer(request):
    customer_stripe = stripe.Customer.retrieve(request.user.stripe_id)
    return Response(status=status.HTTP_200_OK, data=customer_stripe)


@api_view(['GET'])
def get_all_payment(request):
    payment_method = stripe.Customer.list_sources(request.user.stripe_id, object="card")
    return Response(status=status.HTTP_200_OK, data=payment_method)


@api_view(['POST'])
def create_payment_intent(request):
    customer_stripe = stripe.Customer.retrieve(request.user.stripe_id)
    response = stripe.PaymentIntent.create(
        amount=2000,
        payment_method=customer_stripe.default_source,
        currency="usd",
        customer=customer_stripe,
        payment_method_types=["card"],
        confirmation_method="manual"
    )

    return Response(response, status=status.HTTP_200_OK)


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
        default_source=request.data["card_id"]

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
