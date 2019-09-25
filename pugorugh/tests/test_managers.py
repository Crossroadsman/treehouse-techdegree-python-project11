import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref
from pugorugh.managers import AGE_MAPPING

from .base import (VALID_USER_DATA, VALID_USERPREF_DATA, VALID_DOG_DATA,
                   VALID_STATUS_LIST, PugOrUghTestCase)


User = get_user_model()


# Mixins
# ======
class InRangeAssertMixin:
    """Provide assert for within a range (inclusive)"""
    def assertInRange(self, value, low, high):
        if (value < low) or (value > high):
            raise AssertionError(f'{value} is outside range {low} to {high}')


# TestCases
# =========
class DogManagerTests(InRangeAssertMixin, PugOrUghTestCase):

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

    # Tests
    # -----
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
        dogs = Dog.objects.with_genderprefs(self.user)
        
        for dog in dogs:
            self.assertIn(dog.gender, self.user.userpref.gender)

    def test_with_ageprefs_returns_dogs_matching_age_prefs(self):
        self.user.userpref.age = "a"
        self.user.save()
        
        min_age = AGE_MAPPING[1][1]  # 18
        max_age = AGE_MAPPING[2][1]  # 84

        dogs = Dog.objects.with_ageprefs(self.user)
        
        for dog in dogs:
            self.assertInRange(dog.age, min_age, max_age)

    def test_with_sizeprefs_returns_dogs_matching_size_prefs(self):
        self.user.userpref.size = 'm,l'
        self.user.save()

        dogs = Dog.objects.with_sizeprefs(self.user)

        for dog in dogs:
            self.assertIn(dog.size, self.user.userpref.size)

    def test_with_prefs_returns_dogs_matching_all_prefs(self):
        self.user.userpref.size = 's,l'  # lucy/rosie/frankie/ted/dougie
        self.user.userpref.age = 'a'  # lucy/rosie/ted/molly
        self.user.userpref.gender = 'f' # lucy/rosie/frankie/molly
        
        expected_dogs = ['lucy', 'rosie']

        dogs = Dog.objects.with_prefs(self.user).values_list('name', flat=True)

        self.assertEqual(expected_dogs, list(dogs))
