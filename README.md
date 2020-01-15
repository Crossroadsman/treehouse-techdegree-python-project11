Project 11: Pug or Ugh API with Django
======================================

Requirements
------------

The minimum compatible version of Python is 3.6 (December 2016).
Other requirements are specified in [`requirements.txt`][reqs]

Installation
------------

1. Clone the project
2. Create and activate a venv
3. Install dependencies (listed in [`requirements.txt`][reqs])
4. Feel free to use the built-in test superuser (username: admin; password testpassword) or create your
   own user (but note that any user created using the `createsuperuser` command will not be able to use the
   front-end app. If you want a user who is both a superuser for Django Admin purposes AND can use the
   front-end app, first create a user from inside the app then in Django Admin give that user the `staff status`
   and `superuser status` User permissions).

Usage
-----

**TODO**

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

- [ ] Script runs correctly
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
- [ ] `UserDog` Model:
  - [x] Properly configured
  - [x] `user`
  - [x] `dog`
  - [x] `status` ('l'/'d')
  - [ ] Other relevant fields to increase functionality
- [ ] `UserPref` Model:
  - [x] Properly configured
  - [x] `user`
  - [x] `age` ('b'/'y'/'a'/'s')
  - [x] `gender` ('m'/'f')
  - [x] `size` ('s'/'m'/'l'/'xl')
  - [ ] Other relevant fields to increase functionality
- [ ] `Dog` serializer
  - [ ] reveals all fields
- [ ] `UserPref` serializer
  - [ ] reveals all fields except `user`
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


[reqs]: https://github.com/Crossroadsman/treehouse-techdegree-python-project11/blob/master/requirements.txt
