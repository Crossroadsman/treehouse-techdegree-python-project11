import sys
from django.db import models
from django.db.models import Q


AGE_MAPPING = [
    ('b', 4),  # new puppy stage
    ('y', 18),  # remainder of puppy stage
    ('a', 84),  # up to seven years
    ('s', sys.maxsize),  # up to 700 quadrillion years (fingers-crossed for advancements in dog longevity)
]

class DogQuerySet(models.QuerySet):

    # Non user-specific filters
    # -------------------------
    def with_genders(self, genders):
        """Returns all the dogs with genders in the list"""
        return self.filter(gender__in=genders)

    def with_ages(self, low, high):
        """Takes a pair of ages (months) and returns all dogs with an age in 
        the range (inclusive)
        """
        return self.filter(
            age__gte=low,
            age__lte=high
        )

    def with_age_class(self, age_class):
        """Takes an age class ('b', 'y', 'a', 's') and returns all the dogs
        whose age is within the class.
        
        Since the age groups are fuzzy (both in terms of definition AND in
        precision (e.g., a 4 month old dog might be 3.5 months old if owner
        rounds up, or 4.49 months old if owner rounds down)), the transition 
        values return true for both age groups. For example, a person who 
        likes a 'baby' dog is expected to like a 4 month old dog. But a 
        person who likes a 'young' dog probably also likes a 4 month old dog.
        Thus a dog of 4 months will be classified as both baby AND young.
        """
        for i, tup in enumerate(AGE_MAPPING):
            if age_class == tup[0]:
                if i == 0:
                    low = 0
                else:
                    low = AGE_MAPPING[i - 1][1]
                high = tup[1]
                return self.with_ages(low, high)
        
        # value not in age mapping, return empty
        return self.none()

    def with_size_class(self, size_class):
        """Takes a size class ('s', 'm', 'l', 'xl', 'u') and returns all the
        dogs whose size is a match for the class.
        """
        return self.filter(size=size_class)

    # User-specific filters
    # ---------------------
    def with_status(self, user, status):
        """Returns all the dogs that the specified user has 'l'iked or
        'd'isliked or is 'u'ndecided.

        if 'u': status_dogs are any dog without a UserDog for user;
        otherwise, status_dogs are the dogs where the applicable UserDog
        has that status.
        """

        if status == 'u':
            return self.exclude(
                userdog__user=user
            )

        # first dog is first pk with corresponding status
        #
        # Reminder: when querying through a reverseFK or a MTM, the 
        # behaviour of chained filters can be subtly different.
        # Imagine there is a dog called 'Spot'. Current_user has marked
        # Spot as 'l'. Someother_user has marked Spot as 'd'.
        # Now consider the following chained filters. First:
        # dogs_disliked_by_current_user = Dog.objects.filter(
        #     userdog__user=current_user,
        #     userdog__status='d'
        # )
        #
        # This will return exactly what we might expect, a queryset that
        # does not include Spot: he does not have a userdog relation that
        # contains both current_user and 'd'.
        #
        # Second:
        # dogs_reviewed_by_cu_and_disliked_by_someone = Dog.objects.filter(
        #     userdog__user=current_user                
        # ).filter(
        #     userdog__status='d'
        # )
        #
        # Spot WILL appear in this queryset because he does have a userdog
        # relation containing the current_user, so he isn't filtered out
        # by the first filter. He also has a userdog relation with 'd',
        # so he's not filtered out by the second filter.
        return self.filter(
            userdog__user=user,
            userdog__status=status
        )

    # UserPref-specific filters
    # -------------------------
    def with_ageprefs(self, user):
        """Returns all the dogs that match the user's age preferences"""
        age_prefs = set(user.userpref.age.split(","))

        if age_prefs == set([tup[0] for tup in AGE_MAPPING]):
            # all ages are in preferences, no need to refine queryset
            return self.all()
        else: # Use Q objects to OR together the preferences instead of Union
            q_objects = Q()
            for age_class in age_prefs:
                dogs_with_age = self.with_age_class(age_class)
                q_objects |= Q(id__in=dogs_with_age)
            return self.filter(q_objects)

    def with_genderprefs(self, user):
        """Returns all the dogs that match the user's gender preferences"""
        gender_prefs = user.userpref.gender.split(",")
        if "m" in gender_prefs and "f" in gender_prefs:
            # no need to refine queryset
            return self.all()
        else:
            return self.with_genders(gender_prefs)

    def with_sizeprefs(self, user):
        """Returns all the dogs that match the user's size preferences"""
        size_prefs = user.userpref.size.split(",")
        if ("s" in size_prefs and 
                "m" in size_prefs and 
                "l" in size_prefs and 
                "xl" in size_prefs):
            # no need to refine queryset
            return self.all()
        else:  # Use Q objects to OR together the preferences instead of Union
            unknown_size_dogs = self.with_size_class('u')
            q_objects = Q(id__in=unknown_size_dogs)
            for size_class in size_prefs:
                dogs_with_size = self.with_size_class(size_class)
                q_objects |= Q(id__in=dogs_with_size)
            return self.filter(q_objects)

    def with_prefs(self, user):
        """Returns all the dogs that match the user's preferences"""
        return self.with_ageprefs(user).with_genderprefs(user).with_sizeprefs(user)


class DogManager(models.Manager):

    def get_queryset(self):
        return DogQuerySet(self.model, using=self._db)

    def with_status(self, user, status):
        return self.get_queryset().with_status(user, status)

    def with_genderprefs(self, user):
        return self.get_queryset().with_genderprefs(user)

    def with_ageprefs(self, user):
        return self.get_queryset().with_ageprefs(user)

    def with_sizeprefs(self, user):
        return self.get_queryset().with_sizeprefs(user)

    def with_prefs(self, user):
        return self.get_queryset().with_prefs(user)
