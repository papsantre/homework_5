from django.core.management import BaseCommand

from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()
        payment_list = [
            {
                "user_id": 1,
                "pay_date": "2024-10-20",
                "amount": 5000,
                "payment_method": "card",
            },
            {
                "user_id": 2,
                "pay_date": "2024-10-21",
                "amount": 7000,
                "payment_method": "card",
            },
            {
                "user_id": 3,
                "pay_date": "2024-10-22",
                "amount": 2000,
                "payment_method": "cash",
            },
        ]
        payment_creation = []
        for payment in payment_list:
            payment_creation.append(Payment(**payment))
        Payment.objects.bulk_create(payment_creation)
