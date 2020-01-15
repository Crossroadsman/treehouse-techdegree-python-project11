import logging

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import resolve, reverse

from rest_framework.test import APIClient

from .base import VALID_USER_DATA, VALID_DOG_DATA, PugOrUghTestCase

from pugorugh.models import Dog
from pugorugh.views import add_dog, delete_list, delete_dog


User = get_user_model()


class UserRegisterViewTests(PugOrUghTestCase):

    def test_valid_submission_creates_valid_user(self):
        client = APIClient()
        client.post(
            '/api/user/',
            VALID_USER_DATA,
            format='json'
        )

        # Test wil fail if cannot get user
        User.objects.get(username='test_user')


class PugOrUghViewTestCase(PugOrUghTestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        self.abstract = True
        self.kwargs = {}
        self.url = '/dog/'
        self.name = ''
        self.status_code = 200
        self.template = 'pugorugh/'
        self.target_view = None

        self.client = Client()

    # Test Methods
    # ------------
    def test_url_resolves_to_correct_view(self):
        """Ensure that expected URLs resolve to their associated views"""

        if self.abstract:
            return

        resolved_view = resolve(self.url).func

        self.assertEqual(resolved_view, self.target_view)

    def test_view_associated_with_valid_name(self):
        if self.abstract:
            return

        response = self.client.get(reverse(self.name, kwargs=self.kwargs))

        self.assertEqual(response.status_code, self.status_code)

    def test_view_renders_correct_template(self):
        if self.abstract:
            return

        response = self.client.get(reverse(self.name, kwargs=self.kwargs))

        self.assertTemplateUsed(response, self.template)


class AddDogViewTests(PugOrUghViewTestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'add/'
        self.name += 'add_dog'
        self.status_code = 200
        self.template += 'add_dog.html'
        self.target_view = add_dog

        self.image_file = self.make_image_file()
        self.valid_dog_data = {
            'name': VALID_DOG_DATA[0]['name'],
            'age': VALID_DOG_DATA[0]['age'],
            'size': VALID_DOG_DATA[0]['size'],
            'gender': VALID_DOG_DATA[0]['gender'],
            'image': self.image_file
        }

        self.client = Client()

    # Test Methods
    # ------------
    def test_valid_POST_creates_dog(self):

        before_count = Dog.objects.all().count()

        self.client.post(
            reverse(self.name),
            self.valid_dog_data
        )

        dogs = Dog.objects.all()
        dog = dogs.last()

        self.assertEqual(dogs.count(), before_count + 1)
        self.assertEqual(dog.name, self.valid_dog_data['name'])

    def test_valid_POST_redirects_to_index(self):

        response = self.client.post(
            reverse(self.name),
            self.valid_dog_data,
            follow=True
        )

        redirect_chain = response.redirect_chain

        self.assertEqual(
            redirect_chain[-1][0],
            reverse('index')
        )

    def test_invalid_POST_does_not_create_dog(self):

        self.assertEqual(
            Dog.objects.all().count(),
            0
        )

        # no `name`
        invalid_post_data = {
            'age': VALID_DOG_DATA[0]['age'],
            'size': VALID_DOG_DATA[0]['size'],
            'gender': VALID_DOG_DATA[0]['gender']
        }

        response = self.client.post(
            reverse(self.name),
            {**invalid_post_data, 'image': self.image_file}
        )

        logging.debug(f"{response.status_code}\n{response.content.decode()}")

        self.assertEqual(
            Dog.objects.all().count(),
            0
        )

    # renders view on invalid POST
    def test_invalid_POST_renders_correct_view(self):
        # no `name`
        invalid_post_data = {
            'age': VALID_DOG_DATA[0]['age'],
            'size': VALID_DOG_DATA[0]['size'],
            'gender': VALID_DOG_DATA[0]['gender']
        }

        response = self.client.post(
            reverse(self.name),
            {**invalid_post_data, 'image': self.image_file}
        )

        self.assertTemplateUsed(response, self.template)

    # renders view on GET
    # (included in parent TestCase)


class DeleteListViewTests(PugOrUghViewTestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'delete/'
        self.name += 'delete_list'
        self.status_code = 200
        self.template += 'delete_list.html'
        self.target_view = delete_list

        self.create_valid_dog(**VALID_DOG_DATA[0])

        self.client = Client()

    # Test Methods
    # ------------

    # All tests in parent TestCase


class DeleteDogViewTests(PugOrUghViewTestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.kwargs = {'pk': '1'}
        self.url += '<pk>/delete/'
        self.name += 'delete_dog'
        self.status_code = 200
        self.template += 'delete_dog.html'
        self.target_view = delete_dog

        self.create_valid_dog(**VALID_DOG_DATA[0])

        self.client = Client()

    # Test Methods
    # ------------
    def test_url_resolves_to_correct_view(self):
        """Ensure that expected URLs resolve to their associated views"""
        self.url = self.url.replace('<pk>', self.kwargs['pk'])

        resolved_view = resolve(self.url).func

        self.assertEqual(resolved_view, self.target_view)

    def test_confirm_deletes_dog(self):
        before_dogs_count = Dog.objects.all().count()

        self.client.post(
            reverse(self.name, kwargs=self.kwargs),
            {'confirm': 'DELETE'}
        )

        self.assertEqual(
            Dog.objects.all().count(),
            before_dogs_count - 1
        )

    def test_cancel_does_not_delete_dog(self):
        before_dogs_count = Dog.objects.all().count()

        self.client.post(
            reverse(self.name, kwargs=self.kwargs),
            {'cancel': 'Cancel'}
        )

        self.assertEqual(
            Dog.objects.all().count(),
            before_dogs_count
        )
