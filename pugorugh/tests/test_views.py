from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from pugorugh.models import UserPref, Dog, UserDog


User = get_user_model()



VALID_USER_DATA = {
    'username': 'test_user',
    'password': 'test_password'
}

VALID_USERPREF_DATA = {
    # user
    'age': "b,y",
    'gender': 'f',
    'size': 'm,l,xl'
}

VALID_DOG_DATA = {
    'name': 'lucy',
    'image_filename': 'test_image_01.jpg',
    'age': 52,
    'gender': 'f',
    'size': 'l'
}


class UserRegisterViewTests(TestCase):

    def test_valid_submission_creates_valid_user(self):
        client = APIClient()
        client.post(
            '/api/user/',
            VALID_USER_DATA,
            format='json'
        )

        # Test wil fail if cannot get user
        User.objects.get(username='test_user')


class DogRetrieveUpdateAPIViewTests(TestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need:
        # - a user (with token for authentication),
        # - a userprefs, 
        # - at least six dogs to enable
        # - two userdogs for each of 'l', 'd', 'u'

        user = self.create_valid_user()
        self.create_valid_userprefs(user)

        user_data = {
            'username': 'some_test_user',
            'password': 'some_test_password'
        }
        # This user's userprefs must, at a minimum, include the 
        # characteristics of the dogs marked as 'undecided'
        userprefs_data = {
            'age': 'y,a,s',
            'gender': 'm,f',
            'size': 's,m,l,xl'
        }
        
        user2 = self.create_valid_user(**user_data)
        self.create_valid_userprefs(user2, **userprefs_data)

        self.user = user2
        self.token = self.get_token(**user_data)

        test_dog_data = [
            {
                'name': 'rosie',
                'image_filename': 'test_image_02.jpg',
                'age': 20,
                'gender': 'f',
                'size': 'l'
            },
            {
                'name': 'frankie',
                'image_filename': 'test_image_03.jpg',
                'age': 70,
                'gender': 'f',
                'size': 'l'
            },
            {
                'name': 'ted',
                'image_filename': 'test_image_04.jpg',
                'age': 51,
                'gender': 'm',
                'size': 's'
            },
            {
                'name': 'molly',
                'image_filename': 'test_image_05.jpg',
                'age': 25,
                'gender': 'f',
                'size': 'xl'
            },
            {
                'name': 'dougie',
                'image_filename': 'test_image_06.jpg',
                'age': 8,
                'gender': 'm',
                'size': 'l'
            },
        ]

        self.create_valid_dog()
        for dog_data in test_dog_data:
            self.create_valid_dog(**dog_data)

        all_dogs = Dog.objects.all()
        for i, status in enumerate(['l', 'l', 'u', 'u', 'd', 'd']):
            if status == 'u':  # don't create a userdog
                continue
            self.create_valid_userdog(
                user=self.user,
                dog=all_dogs[i],
                status=status
            )

        # print("---- debug setUp() ----")
        # for user in User.objects.all():
        #     print(f'user: {user}')
        #     print(f'userpref: {user.userpref}')
        # for userdog in UserDog.objects.all():
        #     print(f'userdog: {userdog}')
        # print("all dogs:")
        # for dog in all_dogs:
        #     print("{}: {}".format(dog.name, dog.pk))
        # print("---- end debug setUp() ----")


    # Helper Methods
    # --------------
    def create_valid_user(self, **kwargs):
        """Because we are using the DRF to create tokens and the only
        authentication we use is token-based, we need to go through the
        API to create a user, rather than just go straight to the DB.
        """
        client = APIClient()
        if kwargs:
            user_data = kwargs
        else:
            user_data = VALID_USER_DATA
        client.post(
            '/api/user/',
            user_data,
            format='json'
        )

        user = User.objects.get(username=user_data['username'])
        return user

    def get_token(self, **kwargs):
        """We have a dedicated URL where if we POST the user's credentials
        we'll get back their token
        """
        client = APIClient()
        if kwargs:
            user_data = kwargs
        else:
            user_data = VALID_USER_DATA
        response = client.post(
            '/api/user/login/',
            user_data,
            format='json'
        )
        # print("---- helper function: get_token()'s response ----")
        # print(response)
        # print(response.status_code)
        # print(response.data)
        # print("---- end helper function ----")

        return response.data['token']

    def create_valid_userprefs(self, user, **kwargs):
        # the User create process (when going through the API)
        # creates an empty userprefs object. Therefore, we need to
        # check if the corresponding userprefs object already exists
        try:
            userprefs = UserPref.objects.get(user=user)
        except UserPref.DoesNotExist:
            userprefs = UserPref(user=user, **VALID_USERPREF_DATA)

        if kwargs:
            for key, value in kwargs.items():
                setattr(userprefs, key, value)

        userprefs.save()
        return userprefs

    def create_valid_dog(self, **kwargs):
        if kwargs:
            dog = Dog.objects.create(**kwargs)
        else:
            dog = Dog.objects.create(**VALID_DOG_DATA)
        return dog

    def create_valid_userdog(self, user, dog, status):
        userdog = UserDog.objects.create(
            user=user,
            dog=dog,
            status=status
        )
        return userdog
    
    # Tests
    # -----
    def test_getting_dog_pk_negative1_retrieves_first_dog_with_status(self):
        """ Performing a GET with a pk of -1 means get the first relevant
        dog with the specified status ('l' or 'u' or 'd').

        Remember that "relevant" is different for 'u' than for 'l' or 'd':
        'undecided' means: 'I want to see some dogs and apply my stated
        preferences'

        'l' or 'd' means: I want to see some dogs that I already know I
        like or dislike, even if they don't meet my general preferences.
        """
       
        # Include an appropriate "Authorization:" header on all requests.
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        for key, value in {
            'liked': 'lucy',  # 2nd is Rosie
            'undecided': 'frankie',  # 2nd is Ted
            'disliked': 'molly',  # 2nd is Dougie
        }.items():

            status = key
            uri = '/api/dog/-1/{}/next/'.format(status)
            response = client.get(uri)

            # print('---- debug test body: GET response ----')
            # print(response)
            # print(response.status_code)
            # print(response.data)
            # print('---- end debug test body ----')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['name'], value)
        

    def test_getting_dog_pk_positive_retrieves_next_dog_with_status(self):
        # similar to previous test except we want the next (with wraparound)
        # dog with the corresponding status instead of the first
        pass

    def test_putting_a_status_updates_an_existing_userdog_status(self):
        pass

    def test_putting_a_status_creates_a_new_userdog_status(self):
        pass


class UserPrefRetrieveAPIViewTests(TestCase):

    # get the userpref values for a user
    def test_get(self):
        pass

    # put (update) the userpref values for a user
    def test_put(self):
        pass

    # post (create) the userpref values for a user
    def test_post(self):
        pass