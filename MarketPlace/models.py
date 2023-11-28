from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from helpers import *
User = get_user_model()


class MarketPlace(TimestampsModel):
    name = models.CharField(_('market name'), max_length=255)
    cover_image = ExtensionAwareImageField(upload_to='marketplace/cover_images')

    def __str__(self) -> str:
        return self.name
