from django.contrib.auth import get_user_model
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref


User = get_user_model()


class ModelTestCase(TestCase):

    def setUp(self):
        self.abstract = True

        self.test_dog_data = {
            'name': 'lucy',
            'image_filename': 'lucy.jpg',
            'age': 52,
            'gender': 'f',
            'size': 'l',
            'breed': 'labrador retriever'
        }

        self.test_user_data = {
            'username': 'test user'
        }

        self.test_dog = Dog.objects.create(**self.test_dog_data)
        self.test_user = User.objects.create(**self.test_user_data)

        self.test_data = None
        self.test_model = None
        self.test_db_model = None

    def test_create_model_correctly_reflects_data(self):
        """Make sure that the Django model in memory has the right data"""
        if not self.abstract:
            for key, value in self.test_data.items():
                self.assertEqual(
                    value,
                    getattr(self.test_model, key)
                )

    def test_create_saves_valid_model_to_db(self):
        """Make sure that the DB record matches the in-memory model"""
        if not self.abstract:
            self.assertEqual(
                self.test_db_model,
                self.test_model
            )


class DogModelTests(ModelTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False

        self.test_data = self.test_dog_data
        self.test_model = self.test_dog
        self.test_db_model = Dog.objects.get(name=self.test_dog.name)

    def test_str_correctly_represents_model(self):
        self.assertEqual(
            str(self.test_dog),
            self.test_dog.name
        )


class UserDogModelTests(ModelTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False

        self.test_userdog_data = {
            'user': self.test_user,
            'dog': self.test_dog
        }

        self.test_userdog = UserDog.objects.create(**self.test_userdog_data)

        self.test_data = self.test_userdog_data
        self.test_model = self.test_userdog
        self.test_db_model = UserDog.objects.get(
            user=self.test_userdog_data['user'],
            dog=self.test_userdog_data['dog']
        )

