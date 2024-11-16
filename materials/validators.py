from rest_framework.serializers import ValidationError


class ValidateAllowUrl:
    def __init__(self, allow_url):
        self.allow_url = allow_url

    def __call__(self, value_url):
        allow_url = "https://www.youtube.com"
        if value_url.get("video"):
            if not value_url.get("video") in allow_url:
                raise ValidationError(
                    "Необходимо присутствие ссылки на youtube, а не сторонний ресурс"
                )
        return None
