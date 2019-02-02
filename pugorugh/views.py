from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from . import serializers
from . import models


# DRF provides `Request` objects (extensions of Django's HttpRequest).
# One benefit is we can use request.data, which is like request.POST but
# can handle arbitrary data (instead of just form data) and PUT/PATCH in
# addition to POST.
#
# Similarly, DRF has `Request` objects which extend TemplateResponse.
# It takes unordered content and uses 'content negotiation' to determine
# the correct type to return to the client.
class UserRegisterView(CreateAPIView):
    
    # Override the restrictive permissions specified in settings.py
    permission_classes = (permissions.AllowAny,)
    
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class NextDogAPIView(RetrieveAPIView):
    """View for GETting a dog instance"""

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        status = self.kwargs.get('status')
        current_dog_id = self.kwargs.get('pk')
        current_user = self.request.user

        if status not in ['liked', 'disliked']:
            # undecided, therefore get the first dog with no UserDog
            # for the current user.
            #            
            # Note that when querying across relations, the reverse field
            # is called `userdog` not `userdog_set`
            undecided_dogs = self.queryset.exclude(userdog__user=current_user)
            return undecided_dogs[0]

        else:
            # 'l' or 'd'
            status = status[0]
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
            dogs_with_status = self.queryset.filter(
                userdog__user=current_user,
                userdog__status=status
            )
            if dogs_with_status.count() < 2:
                # There are no other dogs with this status
                return self.queryset.none()

            # Try to get a dog with a higher PK
            next_dog = dogs_with_status.filter(id__gt=current_dog_id).first()
            if next_dog is None:
                # wrap back around the dogs and get the first
                next_dog = dogs_with_status.first()
        
        return next_dog


class UserDogCreateUpdateAPIView(
    CreateModelMixin,
    UpdateModelMixin,
    GenericAPIView
):
    """View for POST a new UserDog instance and PUT a change to an existing
    UserDog"""
    
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.DogSerializer

    def create(self, request, *args, **kwargs):
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = models.Dog.objects.get(pk=pk)
        
        # check to see if there is already a UserDog belonging to this
        # user re this dog
        existing = self.queryset.filter(
            user=user, dog=dog
        )
        
        if existing.exists():
            raise ValueError("Shouldn't POST if already exists")


        userdog = models.UserDog.objects.create(
            user=user,
            dog=dog,
            status=status
        )
        
        # What type should create return?
        return userdog

    def update(self, request, *args, **kwargs):
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = models.Dog.objects.get(pk=pk)
        
        # check to see if there is already a UserDog belonging to this
        # user re this dog
        try:
            userdog = self.queryset.get(user=user, dog=dog)
        except models.UserDog.DoesNotExist:
            raise ValueError("Shouldn't PUT if no entry to update")
        
        userdog.status = status
        userdog.save()
        
        # What type should create return?
        return userdog


class UserPrefCreateUpdateAPIView(
    CreateModelMixin,
    UpdateModelMixin,
    GenericAPIView
):
    """View for POST a new set of prefs or PUT a change to existing prefs"""
    
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def create(self, request, *args, **kwargs):
        ### TODO
        pass
        '''
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = models.Dog.objects.get(pk=pk)
        
        # check to see if there is already a UserDog belonging to this
        # user re this dog
        existing = self.queryset.filter(
            user=user, dog=dog
        )
        
        if existing.exists():
            raise ValueError("Shouldn't POST if already exists")


        userdog = models.UserDog.objects.create(
            user=user,
            dog=dog,
            status=status
        )
        
        # What type should create return?
        return userdog
        '''

    def update(self, request, *args, **kwargs):
        ### TODO
        pass
        '''
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = models.Dog.objects.get(pk=pk)
        
        # check to see if there is already a UserDog belonging to this
        # user re this dog
        try:
            userdog = self.queryset.get(user=user, dog=dog)
        except models.UserDog.DoesNotExist:
            raise ValueError("Shouldn't PUT if no entry to update")
        
        userdog.status = status
        userdog.save()
        
        # What type should create return?
        return userdog
        '''
