import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollar(amount):
    """Перевод рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', "USD")
    return int(rate * amount)


def create_stripe_product(prod):
    """Создает продукт в страйпе"""
    product = prod.paid_course if prod.paid_course else prod.paid_lesson
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.get("id")


def create_stripe_price(amount, product_id):
    """Создает цену в страйпе"""
    stripe_price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": product_id},
    )
    return stripe_price.get("id")


def create_stripe_session(stripe_price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": stripe_price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
