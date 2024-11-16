from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import ValidateAllowUrl


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidateAllowUrl(allow_url="video")]


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons_info = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_count_lesson(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ("title", "count_lesson", "lessons_info")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
