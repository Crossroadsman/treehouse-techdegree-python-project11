from django.contrib.auth import get_user_model
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref
from .base import (VALID_USER_DATA, VALID_USERPREF_DATA, VALID_DOG_DATA, VALID_STATUS_LIST, PugOrUghTestCase)

User = get_user_model()


class DogManagerTests(PugOrUghTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # super().setUp()
        
        # Need:
        # - User (with userprefs)
        # - Some dogs
        # - Some UserDogs
        self.user = User.objects.create(**VALID_USER_DATA)
        self.create_valid_userprefs(self.user)
        self.create_some_dogs(VALID_DOG_DATA)
        self.create_some_userdogs(self.user, VALID_STATUS_LIST)


    def test_with_status_returns_dogs_matching_user_and_status(self):
        status = 'l'
        dogs = Dog.objects.with_status(self.user, status).values_list(
            'name',
            flat=True
        )
        userdogs = UserDog.objects.filter(
            user=self.user,
            status=status
        ).values_list(
            'dog__name',
            flat=True
        )
        
        self.assertEqual(list(dogs), list(userdogs))

    def test_with_genderprefs_returns_dogs_matching_gender_prefs(self):
        pass

    def test_with_ageprefs_returns_dogs_matching_age_prefs(self):
        pass

    def test_with_sizeprefs_returns_dogs_matching_size_prefs(self):
        pass

    def test_with_prefs_returns_dogs_matching_all_prefs(self):
        pass
