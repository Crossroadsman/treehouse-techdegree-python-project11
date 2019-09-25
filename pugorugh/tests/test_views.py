from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .base import VALID_USER_DATA


User = get_user_model()


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
