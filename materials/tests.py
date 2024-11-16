from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="usertest@mail.ru")
        self.course = Course.objects.create(
            title="Test Course",
            description="This is a test course",
        )
        self.lesson = Lesson.objects.create(
            title="Lesson Test", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_getting_lesson_retrieve(self):
        self.url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("course"), self.lesson.course.id)

    def test_getting_lesson_create(self):
        self.url = reverse("materials:lesson_create")
        data = {
            "title": "Lesson Test Creation",
            "course": self.course.id,
            "owner": self.user.id,
            "video": "https://www.youtube.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(data.get("title"), "Lesson Test Creation")

    def test_getting_lesson_update(self):
        self.url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Lesson Test Update"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Lesson Test Update")

    def test_getting_lesson_delete(self):
        self.url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_getting_lesson_list(self):
        self.url = reverse("materials:lesson_list")
        response = self.client.get(self.url)
        # print(response.json())
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": None,
                    "preview": None,
                    "video": None,
                    "course": self.course.id,
                    "owner": self.user.id,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="usertest@mail.ru")
        self.course = Course.objects.create(
            title="Test Course",
            description="This is a test course",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("materials:subscription_create")

    def test_subscription_activate(self):
        data = {
            "user": self.user.id,
            "course_id": self.course.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )
        self.assertTrue(Subscription.sign_of_subscription)

    def test_subscription_deactivate(self):
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course_id": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
