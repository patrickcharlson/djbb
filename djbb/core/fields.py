import random
from hashlib import sha1
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import OneToOneField
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, instance, instance_type=None):
        model = self.related.related_model

        try:
            return super(AutoReverseOneToOneDescriptor, self).__get__(instance, instance_type)
        except model.DoesNotExist:
            obj = model(**{self.related.field.name: instance})
            obj.save()
            return super(AutoReverseOneToOneDescriptor, self).__get__(instance, instance_type)


class AutoOneToOneField(OneToOneField):
    """
    OneToOneField creates dependent object on first request from parent object
    if dependent object has not created yet.
    """

    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoReverseOneToOneDescriptor(related))


class ExtendedImageField(models.ImageField):
    """
    Extended ImageField that can resize image before saving it.
    """

    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', None)
        self.height = kwargs.pop('height', None)
        super(ExtendedImageField, self).__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        if data and self.width and self.height:
            content = self.resize_image(data.read(), width=self.width, height=self.height)
            salt = sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            fname = sha1(salt.encode('utf-8') + settings.SECRET_KEY.encode('utf-8')).hexdigest() + '.png'
            data = SimpleUploadedFile(fname, content, content_type='image/png')
        super(ExtendedImageField, self).save_form_data(instance, data)

    def resize_image(self, rawdata, width, height):
        """
        Resize image to fit it into (width, height) box.
        """
        try:
            import Image
        except ImportError:
            from PIL import Image
        image = Image.open(BytesIO(rawdata))
        oldw, oldh = image.size
        if oldw >= oldh:
            x = int(round((oldw - oldh) / 2.0))
            image = image.crop((x, 0, (x + oldh) - 1, oldh - 1))
        else:
            y = int(round((oldh - oldw) / 2.0))
            image = image.crop((0, y, oldw - 1, (y + oldw) - 1))
        image = image.resize((width, height), resample=Image.ANTIALIAS)

        string = BytesIO()
        image.save(string, format='PNG')
        return string.getvalue()
