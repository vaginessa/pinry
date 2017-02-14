from __future__ import unicode_literals

# Assume python2 and fallback for python3
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlsplit as urlparse

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from model_utils.managers import InheritanceManager


class Tag(models.Model):
    """
    Tagging is our only form of organizing pins and we want to try and
    force as much normalization here as possible. Example is if someone has the
    tag Burrito and then someone else uses burrito, this is the same tag. We
    force lowercase because of this.

    We also want to make sure every tag has a nice slug so we can make some
    pretty URLs for tag link sharing.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True) # NOTE: defaults to max_length=50, may need more

    def __unicode__(self):
        return u'{0}'.format(self.title)

    def get_number_of_pins(self):
        pins = self.pin_set.all()
        return len(pins)
    get_number_of_pins.short_description = 'number of pins'

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)


class Pin(models.Model):
    """
    Elements we want every pin to have, all other pins extend this
    model.
    """
    objects = InheritanceManager()

    title = models.CharField(max_length=200)
    url = models.URLField() # NOTE: defaults to max_length=200, may need more
    tags = models.ManyToManyField(Tag, related_name='pins')
    user = models.ForeignKey(User, related_name='pins')

    def __unicode__(self):
        return u'{0}'.format(self.title)

    def get_tags_as_string(self):
        """
        Pretty much only useful for the admin panel.
        """
        return ', '.join(tag.title for tag in self.tags.all())
    get_tags_as_string.short_description = 'tags'

    def add_tag(self, tag_title):
        """
        Instead of trying to create a tag and do this in a view or something
        lets simplify some code.
        """
        try:
            tag = Tag.objects.get(title__iexact=tag_title)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(title=tag_title)
        self.tags.add(tag)

    def remove_tag(self, tag_title):
        """
        If we just added a tag and removed it I don't want misspelled and unused
        tags hanging around in the database. This will help keep the database a
        bit cleaner.
        """
        try:
            tag = Tag.objects.get(title__iexact=tag_title)
        except Tag.DoesNotExist:
            return
        self.tags.remove(tag)
        if len(tag.pin_set.all()) == 0:
            tag.delete()

    def get_url_domain(self):
        """
        Our URL should point to the object being pined, in some cases this
        will be a PDF, Video, Word Document, etc. This is to get a direct link
        to the base website the object is from. Will be used for showing
        favicons mostly.
        """
        return '{0.netloc}'.format(urlparse(self.url))

    def get_image(self):
        """
        All pins should implement this function, the default pin does
        not have an image attached to it but almost all pins should.

        The default return value should be a dictionary::

            return {
                'url': 'http://example.com/image.jpg',
                'width': 300,
                'height': 450,
            }
        """
        return None

    def get_thumbnail(self):
        """
        All pins should implement this function, the default pin does
        not have an image attached to it but almost all pins should.

        The default return value should be a dictionary::

            return {
                'url': 'http://example.com/image.jpg',
                'width': 300,
                'height': 450,
            }
        """
        return None

