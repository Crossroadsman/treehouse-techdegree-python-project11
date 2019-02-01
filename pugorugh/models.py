from django.conf import settings
from django.db.models import Model, CASCADE
from django.db.models import (CharField, PositiveIntegerField, ForeignKey)


class Dog(Model):
    CHOICES = {
        'GENDER': (
            ('m', 'male'),
            ('f', 'female'),
            ('u', 'unknown'),
        ),
        'SIZE': (
            ('s': 'small'),
            ('m': 'medium'),
            ('l': 'large'),
            ('xl': 'extra large'),
            ('u': 'unknown'),
        ),
    }

    name = CharField(max_length=255)
    # most Linux file systems are limited to 255 + 4096, Windows API: 260
    image_filename = CharField(max_length=255)
    breed = CharField(max_length=255)
    age = PositiveIntegerField()  # months
    gender = CharField(max_length=1, choices=CHOICES['GENDER'])
    size = CharField(max_length=2, choices=CHOICES['SIZE'])


class UserMTM(Model):
    CHOICES = {
        'STATUS': (
            ('l', 'liked'),
            ('d', 'disliked'),
        ),
        'AGE': (
            ('b', 'baby'),
            ('y', 'young'),
            ('a', 'adult'),
            ('s', 'senior'),
        ),
        'GENDER': (
            ('m', 'male'),
            ('f', 'female'),
        ),
        'SIZE': (
            ('s', 'small'),
            ('m', 'medium'),
            ('l', 'large'),
            ('xl', 'extra large'),
        )
    }

    class Meta:
        abstract = True


class UserDog(UserMTM):

    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    dog = ForeignKey(to='Dog', on_delete=CASCADE)
    status = CharField(max_length=1, choices=CHOICES['STATUS'])
