import sys
from django.conf import settings
from django.db.models import Model, CASCADE
from django.db.models import (CharField, PositiveIntegerField, ForeignKey, OneToOneField, BooleanField)


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


class UserPref(Model):

    user = OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    age = CharField(max_length=7, default="b,y,a,s")
    gender = CharField(max_length=3, default="m,f")
    size = CharField(max_length=8, default="s,m,l,xl")

    def is_age_in_prefs(self, value):
        mapping = {
            'b': 4,  # new puppy stage
            'y': 12,  # remainder of puppy stage
            'a': 108,  # nine years
            's': sys.maxsize,  # we probably won't see any dogs that live
                                    # beyond nine quintillion months for a while
                                    # this can be computing's 'year 
                                    # 700 quadrillion' problem
        }

        # Since the age groups are fuzzy (both in terms of definition AND in
        # precision (e.g., a 4 month old dog might be 3.5 months old if owner
        # rounds up, or 4.49 months old if owner rounds down)), the transition 
        # values return true for both age groups. For example, a person who 
        # likes a 'baby' dog is expected to like a 4 month old dog. But a 
        # person who likes a 'young' dog probably also likes a 4 month old dog.
        # Thus a dog of 4 months will be classified as both baby AND young.
        in_prefs = False
        if 0 <= value <= mapping['b']:
            in_prefs = 'b' in self.age
        if mapping['b'] <= value <= mapping['y']:
            in_prefs = in_prefs | 'y' in self.age
        if mapping['y'] <= value <= mapping['a']:
            in_prefs = in_prefs | 'a' in self.age
        if mapping['a'] <= value <= mapping['s']:
            in_prefs = in_prefs | 's' in self.age

        return in_prefs

    def is_gender_in_prefs(self, value):
        male_match = False
        female_match = False

        if value == 'm':
            male_match = 'm' in self.gender
        if value == 'f':
            female_match = 'f' in self.gender
        
        return male_match | female_match

    def is_size_in_prefs(self, value):
        # Don't exclude unknown-sized dogs
        if value == 'u':
            return True

        return value in self.size

    def __str__(self):
        return f'{self.user} age: {self.age}, gender: {self.gender}, size: {self.size}'
