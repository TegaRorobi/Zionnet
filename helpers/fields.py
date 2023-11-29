from django.db import models 
from django.core.validators import FileExtensionValidator
from .validators import ImageSizeValidator


class ValidatedImageField(models.ImageField):

    def __init__(self, *args, **kwargs):
        allowed_extensions = kwargs.get('extensions', ('png', 'jpg', 'jpeg', 'jfif'))
        size_validator = ImageSizeValidator(5*1024*1024)
        extension_validator = FileExtensionValidator(allowed_extensions=(allowed_extensions))
        kwargs.setdefault('validators', [size_validator, extension_validator])
        return super().__init__(*args, **kwargs)