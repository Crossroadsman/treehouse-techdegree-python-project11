from django.conf import settings
from django.db.models import Model, CASCADE
from django.db.models import (CharField, PositiveIntegerField, ForeignKey)


class Dog(Model):
    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (UNKNOWN, 'unknown'),
    )
    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    EXTRA_LARGE = 'xl'
    SIZE_CHOICES = (
        (SMALL, 'small'),
        (MEDIUM, 'medium'),
        (LARGE, 'large'),
        (EXTRA_LARGE, 'extra large'),
        (UNKNOWN, 'unknown'),
    )

    name = CharField(max_length=255)
    # most Linux file systems are limited to 255 + 4096, Windows API: 260
    image_filename = CharField(max_length=255)
    breed = CharField(max_length=255)
    age = PositiveIntegerField()  # months
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=2, choices=SIZE_CHOICES)


class UserDog(Model):

    LIKED = 'l'
    DISLIKED = 'd'
    STATUS_CHOICES = (
        (LIKED, 'liked'),
        (DISLIKED, 'disliked'),
    )
    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    dog = ForeignKey(to='Dog', on_delete=CASCADE)
    status = CharField(max_length=1, choices=STATUS_CHOICES)


class UserPref(Model):

    BABY = 'b'
    YOUNG = 'y'
    ADULT = 'a'
    SENIOR = 's'
    AGE_CHOICES = (
        (BABY, 'baby'),
        (YOUNG, 'young'),
        (ADULT, 'adult'),
        (SENIOR, 'senior'),
    )
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    EXTRA_LARGE = 'xl'
    SIZE_CHOICES = (
        (SMALL, 'small'),
        (MEDIUM, 'medium'),
        (LARGE, 'large'),
        (EXTRA_LARGE, 'extra large'),
    )

    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    age = CharField(max_length=1, choices=AGE_CHOICES)
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=2, choices=SIZE_CHOICES)
