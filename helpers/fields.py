from django.db import models 
from django.core.validators import FileExtensionValidator


class ExtensionAwareImageField(models.ImageField):

    def __init__(self, *args, **kwargs):
        allowed_extensions = kwargs.get('extensions', ('png', 'jpg', 'jpeg', 'jfif'))
        extension_validator = FileExtensionValidator(allowed_extensions=(allowed_extensions))
        kwargs['validators'] = list(kwargs.get('validators', [])) + [extension_validator]
        return super().__init__(*args, **kwargs)