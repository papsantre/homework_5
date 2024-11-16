from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from materials.models import Course, Lesson, Subscription
from materials.paginators import Pagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer, SubscriptionSerializer,
)
from users.permissions import IsUserModerator, IsUserOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsUserModerator,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsUserModerator | IsUserOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsUserModerator | IsUserOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsUserModerator,)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = Pagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsUserModerator | IsUserOwner,
        IsAuthenticated,
    )


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsUserModerator | IsUserOwner,
        IsAuthenticated,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        ~IsUserModerator | IsUserOwner,
        IsAuthenticated,
    )


class SubscriptionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    # Определяем набор данных, который будет использоваться
    queryset = Course.objects.all()

    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        # Используем GenericAPIView для получения объекта курса
        course = get_object_or_404(self.get_queryset(), id=course_id)

        # Получаем или создаем подписку
        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if not created:
            # Если подписка уже существует, удаляем ее
            subscription.delete()
            message = "Подписка удалена"
            Subscription.sign_of_subscription = False
        else:
            # Если подписки нет, создаем новую
            message = "Подписка добавлена"
            Subscription.sign_of_subscription = True

        return Response({"message": message})
