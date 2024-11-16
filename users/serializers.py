from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "city",
            "avatar",
        )


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(
        source="payment",
        many=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "avatar",
            "payments",
        )
