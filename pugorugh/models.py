import sys
from django.conf import settings
from django.db.models import Model, CASCADE
from django.db.models import (CharField, PositiveIntegerField, ForeignKey, OneToOneField, BooleanField)

from .managers import DogManager


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

    # Required Fields
    # ---------------
    name = CharField(max_length=255)
    # most Linux file systems are limited to 255 + 4096, Windows API: 260
    image_filename = CharField(max_length=255)
    age = PositiveIntegerField()  # months
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=2, choices=SIZE_CHOICES)

    # Optional Fields
    # ---------------
    breed = CharField(max_length=255, blank=True, default='')

    # Custom Manager
    # --------------
    objects = DogManager()

    class Meta:
        # Make explicit our intent that, unless otherwise specified in a 
        # query, we want to get objects in the order they were created
        ordering = ['pk',]

    def __str__(self):
        return self.name
    

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

    class Meta:
        unique_together = (
            ('user', 'dog'),
        )

    def __str__(self):
        return "{} x {}".format(self.user, self.dog)


class UserPref(Model):

    user = OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    age = CharField(max_length=7, default="b,y,a,s")
    gender = CharField(max_length=3, default="m,f")
    size = CharField(max_length=8, default="s,m,l,xl")

    def __str__(self):
        return f'{self.user} age: {self.age}, gender: {self.gender}, size: {self.size}'
