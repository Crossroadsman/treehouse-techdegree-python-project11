import logging

from django.test import TestCase

from rest_framework import serializers

from pugorugh.serializers import UserPrefSerializer


class UserPrefSerializerTestCase(TestCase):

    def setUp(self):
        self.test_serializer = UserPrefSerializer()
    
    def test_invalid_age_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_age('x')

    def test_repeated_age_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_age('bb')

    def test_invalid_gender_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_gender('q')

    def test_repeated_gender_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_gender('ff')

    def test_invalid_size_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_size('x')

    def test_repeated_size_character_triggers_validationerror(self):
        with self.assertRaises(serializers.ValidationError):
            self.test_serializer.validate_size('ll')
