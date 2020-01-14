import logging
import random

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Prefetch

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from . import serializers
from . import models
from .forms import AddDogForm


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


class RandomDogRetrieveAPIView(RetrieveAPIView):
    """View for getting a random dog"""

    serializer_class = serializers.DogSerializer

    def get_object(self):
        dogs = models.Dog.objects.all()
        dog = random.choice(dogs)
        return dog

class NeedMoreLoveDogRetrieveAPIView(RetrieveAPIView):
    """View for getting a dog that needs more love

    Specifically, we are going to return a random dog from the pool
    of dogs who have the fewest likes. If there are any dogs with no
    likes, this will return a random dog that has no likes. If dog with
    the fewest likes has, say, 3 likes, this will return a random dog
    that has 3 likes.
    """

    serializer_class = serializers.DogSerializer

    def get_object(self):
        # We want to get all the dogs and the count of their likes in
        # UserDog.
    
        # First, create a filtered queryset of UserDogs that Prefetch
        # is going to use:
        likes = models.UserDog.objects.filter(status='l')

        # Now we want to pass a custom Prefetch object into prefetch_related
        # see:
        # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.Prefetch
        fdogs = models.Dog.objects.prefetch_related(
            Prefetch('userdog_set', queryset=likes)
        )
    
        # We can now get the number of likes each dog has by accessing
        # the fdog.userdog_set.count() method
        dog_and_likes_count = [
            (dog.name, dog.userdog_set.count()) for dog in fdogs
        ]
        logging.debug(f"Dogs and Likes Count:\n{dog_and_likes_count}")

        # note that, e.g., Rosie who has 2 likes returns 2 and Muffin, 
        # who has no likes but a dislike returns 0
        # (if we weren't using the filtered prefetch then the count would
        # return 1 for Muffin)
        dog_list = sorted(
            [(dog, dog.userdog_set.count()) for dog in fdogs],
            key=lambda x: x[1]
        )

        unloved = []
        for dog in dog_list:
            if dog[1] > dog_list[0][1]:
                break
            unloved.append(dog[0])

        return random.choice(unloved)


class DogRetrieveUpdateAPIView(
    UpdateModelMixin,
    RetrieveAPIView
):
    """View for GETting a dog instance and setting status"""

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
        status = self.kwargs.get('status')[0]
        current_user = self.request.user

        status_dogs = self.get_queryset().with_status(current_user, status)

        if status == 'u':
            # We want to filter on userprefs to ensure user only sees dogs
            # they might like
            pref_dogs = status_dogs.with_prefs(current_user)
        else:  # 'l' or 'd'
            # Note, we're ignoring userprefs because the user has explicitly
            # expressed a like/dislike for this particular dog. General 
            # preferences shouldn't override this expressed status
            pref_dogs = status_dogs


        first_dog_with_status = pref_dogs.first()

        # print("\n==== DEBUG DogRetrieveUpdateAPIView.get_first_dog_with_status ====")
        # print(f'status: {status}')
        # print(f'current_user: {current_user}')
        # print(f'userpref: {current_user.userpref}')

        # print(f'status_dogs: {status_dogs}')
        # for dog in status_dogs:
        #     print(f'{dog.name}: {dog.pk}')
        # print(f'pref_dogs: {pref_dogs}')
        # for dog in pref_dogs:
        #     print(f'{dog.name}: {dog.pk}')
        # print(f'first with status: {first_dog_with_status}')
        # print("==== END DEBUG DogRetrieveUpdateAPIView.get_first_dog_with_status ====\n")

        return first_dog_with_status

    def get_next_dog_with_status(self):
        """returns the next dog (pk order, wraparound) with the corresponding
        status (empty queryset if none)
        """
        status = self.kwargs.get('status')[0]
        current_user = self.request.user
        current_dog_pk = int(self.kwargs.get('pk'))

        status_dogs = self.get_queryset().with_status(current_user, status)

        if status == 'u':
            # first dog is the next pk with no corresponding userdog
            # We want to filter on userprefs to ensure user only sees dogs
            # they might like
            pref_dogs = status_dogs.with_prefs(current_user)
        else:  # 'l' or 'd'
            # first dog is next in pk with same userdog status
            #
            # Note, we're ignoring userprefs because the user has explicitly
            # expressed a like/dislike for this particular dog. General 
            # preferences shouldn't override this expressed status
            pref_dogs = status_dogs

        next_pref_dog = pref_dogs.filter(
            id__gt=current_dog_pk
        ).first()

        # if there are no higher pks with status, wraparound to first
        if next_pref_dog is None:
            next_pref_dog = pref_dogs.first()

        # print("\n==== DEBUG DogRetrieveUpdateAPIView.get_next_dog_with_status ====")
        # print(f'status: {status}')
        # print(f'current_user: {current_user}')
        # print(f'status_dogs: {status_dogs}')
        # print(f'pref_dogs: {pref_dogs}')
        # print(f'next with status: {next_pref_dog}')
        # print("==== END DEBUG DogRetrieveUpdateAPIView.get_next_dog_with_status ====\n")

        return next_pref_dog

    # APIView Methods
    # ---------------
    def get_object(self):
        current_dog_id = int(self.kwargs.get('pk'))

        # print("\n==== DEBUG DogRetrieveUpdateAPIView.get_object ====")
        # print(f'current_dog_id: {current_dog_id}')
        # print("==== END DEBUG DogRetrieveUpdateAPIView.get_object ====\n")

        # if pk is -1 (switching categories)
        # get the first dog in the category (wrapping around if necessary)
        if current_dog_id == -1:
            dog = self.get_first_dog_with_status()

            # print("--- DEBUG get_object: entering pk==-1 branch ----")
            # print(f'first_dog: {dog}')
            # print("--- END DEBUG get_object: entering pk==-1 branch ----")


        # pk is not -1 (it's a real pk)
        # get the first dog with the matching status with a pk > current_dog_id
        # (wrap around if necessary).
        else:
            dog = self.get_next_dog_with_status()
            # print("--- DEBUG get_object: entering pk!=-1 branch ----")
            # print(f'next_dog: {dog}')
            # print("--- END DEBUG get_object: entering pk!=-1 branch ----")

        #If no dogs at all with status, return 404
        if dog is None:
            raise NotFound(detail="Error 404, page not found", code=404)
        else:
            return dog

    # Mixin Methods
    # -------------
    def update(self, request, *args, **kwargs):
        status = self.kwargs.get('status')[0]
        user = self.request.user
        pk = self.kwargs.get('pk')
        dog = self.get_queryset().get(pk=pk)

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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserPrefRetrieveAPIView(
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveAPIView
):
    """Return the UserPref values for a user"""
    # GET /api/user/preferences

    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    # Override Retrieve Methods
    # -------------------------
    def get_object(self):
        user = self.request.user
        userpref = self.get_queryset().filter(user=user).first()
        if userpref is None:
            raise NotFound(detail="Error 404, page not found", code=404)
        else:
            return userpref

    # Mixin Methods
    # -------------
    def update(self, request, *args, **kwargs):
        userpref = self.get_object()
        
        serializer = self.get_serializer(userpref, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # just calls serializer.save()

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_create(self, request, *args, **kwargs):
        
        # serializer is guaranteed to be passed in as a kwarg
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


def add_dog(request):
    if request.method == "POST":
        # submit dog
        form = AddDogForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    
    else:  # GET
        form = AddDogForm()
    
    template = 'pugorugh/add_dog.html'
    context = {'form': form}
    return render(request, template, context)


def delete_list(request):
    dogs = models.Dog.objects.all()
    template = 'pugorugh/delete_list.html'
    context = {'dogs': dogs}
    return render(request, template, context)


def delete_dog(request, pk):
    dog = get_object_or_404(models.Dog, pk=pk)

    if request.method == "POST":

        if 'confirm' in request.POST:  # delete the dog
            logging.debug(f"deleting {dog.name} ({dog.pk})...")
            dog.delete()
            logging.debug(f"Deleted dog. Remaining dogs: {models.Dog.objects.all()}")
            return redirect(reverse('index'))

        else:  # do not delete the dog, go back to previous screen
            return redirect(reverse('delete_list'))

    else:  # GET
        template = 'pugorugh/delete_dog.html'
        context = {'dog': dog}
        return render(request, template, context)
