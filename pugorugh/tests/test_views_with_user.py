from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from pugorugh.models import UserPref, Dog, UserDog
from .base import (VALID_USER_DATA, VALID_USERPREF_DATA, VALID_DOG_DATA,
                   VALID_STATUS_LIST, PugOrUghTestCase)


User = get_user_model()


class ViewsWithUserTestCase(PugOrUghTestCase):
    """This subclass defines the common requirements for testing views
    that depend on an authenticated user being available
    """

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need:
        # - a user (with token for authentication),
        # - a userprefs,
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

        return response.data['token']

    def authenticate_user(self):
        """Ensure that all requests will have appropriate `Authorization: `
        headers
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        return client

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

    def debug_print_response_details(self, response):
        print('==== DEBUG response details ====')
        print('---- full response ----')
        print(response)
        print('---- end full response ----')
        print(f'status code: {response.status_code}')
        if hasattr(response, 'data'):
            print(f'data: {response.data}')
        print('==== END DEBUG response details ====')


class DogRetrieveUpdateAPIViewTests(ViewsWithUserTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need ((s) from super):
        # - (s) a user (with token for authentication),
        # - (s) a userprefs,
        # - at least six dogs to enable
        # - two userdogs for each of 'l', 'd', 'u'
        super().setUp()

        self.create_some_dogs(VALID_DOG_DATA)
        self.create_some_userdogs(self.user, VALID_STATUS_LIST)

        self.client = self.authenticate_user()

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

        for key, value in {
            'liked': 'lucy',  # 2nd is Rosie
            'undecided': 'frankie',  # 2nd is Ted
            'disliked': 'molly',  # 2nd is Dougie
        }.items():

            status = key
            uri = '/api/dog/-1/{}/next/'.format(status)
            response = self.client.get(uri)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['name'], value)

    def test_getting_dog_pk_positive_retrieves_next_dog_with_status(self):
        """similar to previous test except we want the next (with wraparound)
        dog with the corresponding status instead of the first
        """

        for key, values in {
            'liked': ['lucy', 'rosie'],
            'undecided': ['frankie', 'ted'],
            'disliked': ['molly', 'dougie']
        }.items():
            for i, name in enumerate(values):
                expected_next_dog_name = values[(i + 1) % len(values)]

                status = key
                object = Dog.objects.get(name=name)
                uri = f'/api/dog/{object.pk}/{status}/next/'
                response = self.client.get(uri)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data['name'], expected_next_dog_name)

    def test_getting_invalid_pk_returns_404(self):
        """If there are no dogs with the relevant status, return a 404"""

        # unlike all liked dogs
        likes = UserDog.objects.filter(
            user=self.user,
            status='l'
        )
        for userdog in likes:
            userdog.status = 'u'
            userdog.save()

        # Note the actual PK doesn't matter (as long as it is a postive
        # integer) when asking for the next dog.
        uri = '/api/dog/1/liked/next/'

        response = self.client.get(uri)

        self.assertEqual(response.status_code, 404)

    def test_putting_status_updates_an_existing_explicit_userdog_status(self):
        """ liked <---> disliked """
        pk = 1  # liked
        userdog = UserDog.objects.get(dog=pk)
        old_status = userdog.status
        expected_old_status = 'l'

        uri = f'/api/dog/{userdog.dog.pk}/disliked/'
        self.client.put(uri)

        expected_new_status = 'd'
        userdog = UserDog.objects.get(dog=pk)

        self.assertEqual(old_status, expected_old_status)
        self.assertEqual(userdog.status, expected_new_status)

    def test_putting_status_creates_a_new_userdog_status(self):
        """ undecided --> [liked | disliked] """
        pk = 3  # undecided
        with self.assertRaises(UserDog.DoesNotExist):
            userdog = UserDog.objects.get(dog=pk)

        uri = f'/api/dog/{pk}/liked/'
        self.client.put(uri)

        expected_new_status = 'l'
        userdog = UserDog.objects.get(dog=pk)

        self.assertEqual(userdog.status, expected_new_status)

    def test_putting_status_deletes_an_existing_explicit_userdog_status(self):
        """ [liked | disliked] --> undecided """
        pk = 5  # disliked
        userdog = UserDog.objects.get(dog=pk)
        old_status = userdog.status
        expected_old_status = 'd'

        uri = f'/api/dog/{userdog.dog.pk}/undecided/'
        self.client.put(uri)

        self.assertEqual(old_status, expected_old_status)
        with self.assertRaises(UserDog.DoesNotExist):
            userdog = UserDog.objects.get(dog=pk)


class RandomDogRetrieveAPIViewTests(ViewsWithUserTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need ((s) from super):
        # - (s) a user (with token for authentication),
        # - (s) a userprefs,
        # - at least six dogs to enable
        # - two userdogs for each of 'l', 'd', 'u'
        super().setUp()

        self.create_some_dogs(VALID_DOG_DATA)
        self.create_some_userdogs(self.user, VALID_STATUS_LIST)

        self.client = self.authenticate_user()

    # Tests
    # -----
    def test_view_retrieves_a_dog(self):
        dog_names = [x['name'] for x in VALID_DOG_DATA]
        uri = '/api/dog/random/'

        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['name'], dog_names)


class NeedMoreLoveDogRetrieveAPIView(ViewsWithUserTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need ((s) from super):
        # - (s) a user (with token for authentication),
        # - (s) a userprefs,
        # - at least six dogs to enable
        # - two userdogs for each of 'l', 'd', 'u'
        super().setUp()

        self.create_some_dogs(VALID_DOG_DATA)
        self.create_some_userdogs(self.user, VALID_STATUS_LIST)

        self.client = self.authenticate_user()

    # Tests
    # -----
    def test_view_retrieves_an_unloved_dog(self):
        dog_names = [
            'frankie',
            'ted',
            'molly',
            'dougie'
        ]
        uri = '/api/dog/needs-love/'

        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['name'], dog_names)


class UserPrefRetrieveAPIViewTests(ViewsWithUserTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        # Need ((s) from super):
        # - (s) a user (with token for authentication),
        # - (s) a userprefs,
        super().setUp()
        self.client = self.authenticate_user()

    # Tests
    # -----
    def test_get_returns_userprefs_for_current_user(self):
        uri = '/api/user/preferences/'

        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        for field in ['age', 'gender', 'size']:
            self.assertEqual(
                getattr(self.user.userpref, field),
                response.data[field]
            )

    # put (update) the userpref values for a user
    def test_put_updates_userprefs_for_current_user(self):
        uri = '/api/user/preferences/'

        new_prefs = {
            'age': 'y',
            'gender': 'm',
            'size': 's,xl'
        }

        response = self.client.put(
            uri,
            new_prefs,
            format='json'
        )

        # print('==== DEBUG test body: PUT response ====')
        # self.debug_print_response_details(response)
        # print('==== END DEBUG test body: PUT response ====')

        self.assertEqual(response.status_code, 200)
        for field in ['age', 'gender', 'size']:
            self.assertEqual(
                new_prefs[field],
                getattr(self.user.userpref, field)
            )
