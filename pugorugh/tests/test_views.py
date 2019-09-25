from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient


User = get_user_model()


VALID_USER_DATA = {
    'username': 'test_user',
    'password': 'test_password'
}


class UserRegisterViewTests(TestCase):

    def test_valid_submission_creates_valid_user(self):
        client = APIClient()
        client.post(
            '/api/user/',
            VALID_USER_DATA,
            format='json'
        )

        # Test wil fail if cannot get user
        User.objects.get(username='test_user')
