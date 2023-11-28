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


class Store(TimestampsModel):
    marketplace = models.ForeignKey(MarketPlace, related_name='stores', on_delete=models.PROTECT)
    vendor = models.ForeignKey(User, verbose_name=_('store vendor'), related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(_('store name'), max_length=255)
    description = models.TextField(_('store description'), null=True, blank=True)
    logo = ExtensionAwareImageField(upload_to='store/logos', null=True, blank=True)
    cover_image = ExtensionAwareImageField(upload_to='store/cover_images', null=True, blank=True)
    country = models.CharField(_('country of location'), max_length=255)
    city = models.CharField(_('store city'), max_length=255)
    province = models.CharField(_('store province'), max_length=255)
    additional_information = models.JSONField(_('store additional information'), null=True, blank=True)

    def __str__(self) -> str:
        return self.name.__str__()
