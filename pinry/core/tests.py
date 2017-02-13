from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from .models import Tag
from .models import Pin


class TagModelTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(title="burrito")
        Tag.objects.create(title="taco")
        Tag.objects.create(title="burrito & taco") # test slugify
        Tag.objects.create(title="Quesadilla") # test lowercase

    def test_tag_titles(self):
        burrito = Tag.objects.get(title__iexact="burrito")
        taco = Tag.objects.get(title__iexact="taco")
        burrito_and_taco = Tag.objects.get(title__iexact="burrito & taco")
        quesadilla = Tag.objects.get(title__iexact="Quesadilla")

        self.assertEqual(burrito.title, "burrito")
        self.assertEqual(taco.title, "taco")
        self.assertEqual(burrito_and_taco.title, "burrito & taco")
        self.assertEqual(quesadilla.title, "quesadilla") # should lowercase q

    def test_tag_slugs(self):
        burrito = Tag.objects.get(title__iexact="burrito")
        taco = Tag.objects.get(title__iexact="taco")
        burrito_and_taco = Tag.objects.get(title__iexact="burrito & taco")
        quesadilla = Tag.objects.get(title__iexact="Quesadilla")

        self.assertEqual(burrito.slug, "burrito")
        self.assertEqual(taco.slug, "taco")
        self.assertEqual(burrito_and_taco.slug, "burrito-taco") # should nix &
        self.assertEqual(quesadilla.slug, "quesadilla")

    def test_tag_get_number_of_pins(self):
        pass


class PinModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="overshard")
        Pin.objects.create(title="Pinry on GitHub",
                url="https://github.com/pinry/pinry", user=user)
        Tag.objects.create(title="django")
        Tag.objects.create(title="rails")

    def test_pin_fields(self):
        piney_on_github = Pin.objects.get(
                title="Pinry on GitHub")
        user = User.objects.get(username="overshard")
        self.assertEqual(piney_on_github.title, "Pinry on GitHub")
        self.assertEqual(piney_on_github.url,
                "https://github.com/pinry/pinry")
        self.assertEqual(piney_on_github.user, user)

    def test_pin_functions(self):
        piney_on_github = Pin.objects.get(
                title="Pinry on GitHub")
        self.assertEqual(piney_on_github.get_url_domain(), "github.com")
        self.assertEqual(piney_on_github.get_image_url(), None)

    def test_pin_add_tag(self):
        piney_on_github = Pin.objects.get(
                title="Pinry on GitHub")
        piney_on_github.add_tag("code")
        piney_on_github.add_tag("open source")
        # Test adding existing tag
        piney_on_github.add_tag("django")
        code_tag = Tag.objects.get(title="code")
        open_source_tag = Tag.objects.get(title="open source")
        django_tag = Tag.objects.get(title="django")
        rails_tag = Tag.objects.get(title="rails")
        # Now make sure the tags exist on the pin
        self.assertIn(code_tag, piney_on_github.tags.all())
        self.assertIn(open_source_tag, piney_on_github.tags.all())
        self.assertIn(django_tag, piney_on_github.tags.all())
        self.assertNotIn(rails_tag, piney_on_github.tags.all())

    def test_pin_remove_tag(self):
        pass

    def test_pin_get_tags_as_string(self):
        pass


class TagAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="overshard",
                password="secret")
        self.client.login(username="overshard", password="secret")

    def test_tag_api(self):
        django_tag_post = self.client.post("/api/tags/", {"title": "django"})
        self.assertEqual(django_tag_post.status_code, 201)


class PinAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="overshard",
                password="secret")
        self.client.login(username="overshard", password="secret")

    def test_pin_api(self):
        piney_on_github_post = self.client.post("/api/pins/?format=json",
                {"title": "Pinry on GitHub",
                "url": "https://github.com/pinry/pinry",
                "tags": [{"title": "django"}, {"title": "open source"}]},
                format="json")
        self.assertEqual(piney_on_github_post.status_code, 201)

        piney_on_github_get = self.client.get("/api/pins/1/")
        self.assertEqual(piney_on_github_get.status_code, 200)

        django_tag_get = self.client.get("/api/tags/1/")
        self.assertEqual(django_tag_get.status_code, 200)
        open_source_tag_get = self.client.get("/api/tags/2/")
        self.assertEqual(open_source_tag_get.status_code, 200)

