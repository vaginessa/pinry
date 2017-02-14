from cStringIO import StringIO
import os

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from PIL import Image

from pinry.core.models import Pin


class ImagePin(Pin):
    image = models.ImageField(upload_to="image-pin/images",
            height_field='image_height', width_field='image_width')
    image_width = models.PositiveIntegerField(blank=True)
    image_height = models.PositiveIntegerField(blank=True)

    thumbnail = models.ImageField(upload_to="image-pin/thumbnails",
            height_field='thumbnail_height', width_field='thumbnail_width',
            blank=True, null=True)
    thumbnail_width = models.PositiveIntegerField(blank=True, null=True)
    thumbnail_height = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(ImagePin, self).save(*args, **kwargs)
	if not self.thumbnail:
	    self.make_thumbnail()

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        fh = storage.open(self.image.name, 'r')
        try:
            pil = Image.open(fh)
        except:
            return False

        pil.thumbnail((240, 10000), Image.ANTIALIAS)
        fh.close()

        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(os.path.split(self.image.name)[-1])
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            raise Exception('Invalid file type.')

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = StringIO()
        pil.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()

    def get_image(self):
        return {
            'url': self.image.url,
            'width': self.image_width,
            'height': self.image_height,
        }

    def get_thumbnail(self):
        return {
            'url': self.thumbnail.url,
            'width': self.thumbnail_width,
            'height': self.thumbnail_height,
        }

