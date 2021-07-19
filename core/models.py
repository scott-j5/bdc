from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]