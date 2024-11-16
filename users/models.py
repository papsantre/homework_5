from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="email",
    )
    phone_number = PhoneNumberField(
        blank=True,
        region="RU",
        verbose_name="номер телефона",
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="город",
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        blank=True,
        null=True,
        verbose_name="аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="payment",
        blank=True,
        null=True,
    )
    pay_date = models.DateField(
        verbose_name="Дата",
        help_text="Укажите дату оплаты",
        blank=True,
        null=True,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
        related_name="payment_course",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
        related_name="payment_lesson",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма",
        help_text="Укажите сумму оплаты",
    )
    payment_method = models.CharField(
        max_length=15,
        choices=(("cash", "наличными"), ("card", "картой")), blank=True,
        null=True,
    )
    session_id = models.CharField(max_length=255,
                                  verbose_name='ID сессии',
                                  blank=True,
                                  null=True, )
    link_to_payment = models.URLField(max_length=400,
                                      verbose_name='ссылка на оплату',
                                      blank=True,
                                      null=True, )

    def __str__(self):
        return f"{self.user} - {self.amount} руб."

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
