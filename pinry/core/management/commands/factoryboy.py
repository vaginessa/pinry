from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Factory

from piney.core.models import Tag
from piney.core.models import Pin


class Command(BaseCommand):
    help = 'Creates many fake pins for testing'

    def handle(self, *args, **kwargs):
        faker = Factory.create()
        user = User.objects.create_user(username=''.join(faker.words(nb=1)))
        for i in range(100):
            pin = Pin(title=' '.join(faker.words()), url=faker.url(),
                    user=user)
            pin.save()
            for n in range(3):
                pin.add_tag(''.join(faker.words(nb=1)))

