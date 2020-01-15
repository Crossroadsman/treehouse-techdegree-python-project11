Project 11: Pug or Ugh API with Django
======================================

Requirements
------------

The minimum compatible version of Python is 3.6 (December 2016).
Other requirements are specified in [`requirements.txt`][reqs]. Additional
requirements for packages that might be useful for testing but not required
to use the application are specified in [`test-requirements.txt`][testreqs].

Installation
------------

1. Clone the project
2. Create and activate a venv
3. Install dependencies (listed in [`requirements.txt`][reqs])
4. Feel free to use one of the built-in users:
   
   Username | Password       | User Type
   ---------|----------------|-----------
   `admin`  | `testpassword` | superuser (for admin functions)
   `alice`  | `testpassword` | application user (for using the app)

   or create your own user (**but Note that any user created using the
   `createsuperuser` command will not be able to use the front-end app. If you
   want a user who is both a superuser for Django Admin purposes AND can use
   the front-end app, first create a user from inside the app then in Django
   Admin give that user the `staff status` and `superuser status` User
   permissions).

Usage
-----

- The application can be run using `python3 manage.py runserver 0:8000`
- Tests can be run using `python3 manage.py test`
- Coverage reports can be generated using `coverage run manage.py test`

Project Status
--------------

### vs Specs from Project Instructions ###

- [x] Create application with the following models and fieldnames:
  - [x] `Dog` model
    - [x] `name`
    - [x] `image_filename`
    - [x] `breed`
    - [x] `age` (integer for months)
    - [x] `gender` ('m' for male, 'f' for female, 'u' for unknown)
    - [x] `size` ('s' small, 'm' medium, 'l' large, 'xl' extra large,
          'u' unknown)
  - [x] `UserDog` model
    - [x] `user`
    - [x] `dog`
    - [x] `status` ('l' liked, 'd' disliked)
  - [x] `UserPref` model
    - [x] `user`
    - [x] `age` ('b' baby, 'y' young, 'a' adult, 's' senior)
    - [x] `gender` ('m' male, 'f' female)
    - [x] `size` ('s' small, 'm' medium, 'l' large, 'xl' extra large)
- [x] Create serializers:
  - [x] `Dog` (all fields need to be revealed)
  - [x] `UserPref` (all fields need to be revealed except `user`)
- [x] Create routes:
  - [x] get dogs:
    - [x] next liked: `/api/dog/<pk>/liked/next/`
    - [x] next disliked: `/api/dog/<pk>/disliked/next/`
    - [x] next undecided: `/api/dog/<pk>/undecided/next/`
  - [x] set dog's status:
    - [x] like: `/api/dog/<pk>/liked/`
    - [x] dislike: `/api/dog/<pk>/disliked/`
    - [x] undecided: `/api/dog/<pk>/undecided/`
  - [x] set user preferences:
    - [x] `/api/user/preferences/`
- [x] The supplied project uses Token-based Auth. This functionality should be
      maintained.
- [x] Unit Tests
- [x] Allow addition/deletion of dogs to the site
- [x] Add additional data fields to the models to increase app functionality
- [x] Add additional routes to the site to increase functionality
- [x] >75% Test coverage

### vs Specs from How You Will Be Graded ###

- [x] Script runs correctly
- [x] Correct dogs are shown
- [x] Ability to add/remove dogs
- [x] `Dog` Model:
  - [x] Properly configured
  - [x] `name`
  - [x] `image_filename`
  - [x] `breed`
  - [x] `age` (integer months)
  - [x] `gender` ('m'/'f'/'u')
  - [x] `size` ('s'/'m'/'l'/'xl')
  - [x] Other relevant fields to increase functionality
- [x] `UserDog` Model:
  - [x] Properly configured
  - [x] `user`
  - [x] `dog`
  - [x] `status` ('l'/'d')
  - [x] Other relevant fields to increase functionality
- [x] `UserPref` Model:
  - [x] Properly configured
  - [x] `user`
  - [x] `age` ('b'/'y'/'a'/'s')
  - [x] `gender` ('m'/'f')
  - [x] `size` ('s'/'m'/'l'/'xl')
  - [x] Other relevant fields to increase functionality
- [x] `Dog` serializer
  - [x] reveals all fields
- [x] `UserPref` serializer
  - [x] reveals all fields except `user`
- [x] Routes:
  - [x] next dog:
    - [x] next liked: `/api/dog/<pk>/liked/next/`
    - [x] next disliked: `/api/dog/<pk>/disliked/next/`
    - [x] next undecided: `/api/dog/<pk>/undecided/next/`
  - [x] set dog's status:
    - [x] like: `/api/dog/<pk>/liked/`
    - [x] dislike: `/api/dog/<pk>/disliked/`
    - [x] undecided: `/api/dog/<pk>/undecided/`
  - [x] set user preferences:
    - [x] `/api/user/preferences/`
  - [x] additional routes that increase functionality
- [x] Token-based Auth
- [x] Unit Tests
  - [x] >50% coverage
  - [x] >75% coverage
- [x] PEP8 Compliant

Testing
-------

### [Test Running](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#running-tests) ###

- Run all tests:
  ```console
   $ python3 manage.py test
   ```

- Run a single test suite:
  ```console
  $ python3 manage.py test pugorugh
  ```

- Run a single test file:
  ```console
  $ python3 manage.py test pugorugh.tests.test_models
  ```

- Run a single test case:
  ```console
  $ python3 manage.py test pugorugh.tests.test_models.DogModelTests
  ```

- Run a single test method:
  ```console
  $ python3 manage.py test accounts.tests.test_models.MenuModelTests.test_create_model_database_has_correct_data
  ```

### Coverage ###

- Run coverage:
  ```console
  $ coverage run manage.py test [the-app-to-test]
  ```

- Show the simple coverage report:
  ```console
  $ coverage report
  ```

- Generate a detailed HTML report (after coverage has been run):
  ```console
  $ coverage html
  ```

- Erase the coverage report
  ```console
  $ coverage erase
  ```


[reqs]: https://github.com/Crossroadsman/treehouse-techdegree-python-project11/blob/master/requirements.txt
[testreqs]: https://github.com/Crossroadsman/treehouse-techdegree-python-project11/blob/master/test-requirements.txt
