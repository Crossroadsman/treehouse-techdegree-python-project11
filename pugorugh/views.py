from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

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

    # Attributes
    # ----------
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    # Helper Methods
    # --------------
    def get_first_dog_with_status(self):
        """returns the first dog for the current user with the corresponding
        status (empty queryset if not dog with status)
        """
        status = self.kwargs.get('status')
        current_user = self.request.user

        if status[0] not in ['l', 'd']:
            # first dog is the first pk with no corresponding userdog
            undecided_dogs = self.get_queryset().exclude(
                userdog__user=current_user
            )
            first_dog_with_status = undecided_dogs.first()

        else:
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
            status_dogs = self.get_queryset().filter(
                userdog__user=current_user,
                userdog__status=status[0]
            )
            first_dog_with_status = status_dogs.first()
        return first_dog_with_status

    def get_next_dog_with_status(self):
        """returns the next dog (pk order, wraparound) with the corresponding
        status (empty queryset if none)
        """
        status = self.kwargs.get('status')
        current_user = self.request.user
        current_dog_pk = self.kwargs.get('pk')

        if status[0] not in ['l', 'd']:
            # first dog is the next pk with no corresponding userdog
            status_dogs = self.get_queryset().exclude(
                userdog__user=current_user
            )

        else:  # 'l' or 'd'
            # first dog is next in pk with same userdog status
            status_dogs = self.get_queryset().filter(
                userdog__user=current_user,
                userdog__status=status[0]
            )

        next_dog_with_status = status_dogs.filter(
            id__gt=current_dog_pk
        ).first()

        # if there are no higher pks with status, wraparound to first
        if next_dog_with_status is None:
            next_dog_with_status = status_dogs.first()

        return next_dog_with_status

    # APIView Methods
    # ---------------
    def get_object(self):
        current_dog_id = self.kwargs.get('pk')

        # if pk is -1 (switching categories)
        # get the first dog in the category (wrapping around if necessary)
        if current_dog_id == -1:
            dog = self.get_first_dog_with_status()

        # pk is not -1 (it's a real pk)
        # get the first dog with the matching status with a pk > current_dog_id
        # (wrap around if necessary).
        else:
            dog = self.get_next_dog_with_status()

        #If no dogs at all with status, return 404
        if dog is None:
            raise NotFound(detail="Error 404, page not found", code=404)
        else:
            return dog


# We should be able to mixin the update view to the retrieve view.


class DogStatusUpdateAPIView(UpdateAPIView):
    """View for setting the UserDog status for a particular dog"""

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def update(self, request, *args, **kwargs):
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = self.get_queryset().get(pk=pk)

        print("=== DEBUG ===")
        print("Setting a UserDog with the following values:")
        print(f'status: {status}')
        print(f'user: {user}')
        print(f'dog pk: {pk}')
        print(f'dog: {dog}')

        if status in ['l', 'd']:

            # try to get the specified userdog
            userdog = dog.userdog_set.filter(user=user).first()

            if userdog:
                # update the userdog
                userdog.status = status
                userdog.save()
            else:  # no userdog
                # create the userdog
                userdog = models.UserDog.objects.create(
                    user=user,
                    dog=dog,
                    status=status
                )
            
        if status == 'u':
            userdog = dog.userdog_set.filter(user=user).first()
            if userdog:
                userdog.delete()

        serializer = self.get_serializer(dog)
        return Response(serializer.data)




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
