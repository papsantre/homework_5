from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.services import create_stripe_product, convert_rub_to_dollar, create_stripe_price, create_stripe_session
from users.models import User, Payment
from users.permissions import IsUserProfileOwner, IsUserOwner
from users.serializers import UserSerializer, PaymentSerializer, UserCreateSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (
        IsUserProfileOwner,
        IsAuthenticated,
    )


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (
        IsAuthenticated,
        IsUserOwner,
    )


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (
        IsAuthenticated,
        IsUserOwner,
    )


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (
        IsAuthenticated,
        IsUserOwner,
    )


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_dollar = convert_rub_to_dollar(payment.amount)
        product_id = create_stripe_product(payment)
        stripe_price = create_stripe_price(amount_dollar, product_id)
        session_id, payment_link = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.link_to_payment = payment_link
        payment.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["pay_date"]
    filterset_fields = ["payment_method", "paid_course", "paid_lesson"]
