Project 11: Pug or Ugh API with Django
======================================

Installation
------------
1. Clone the project
2. Create and activate a venv
3. Install dependencies (listed in requirements.txt)

Usage
-----
**TODO**

Project Status
--------------
### vs Specs from Project Instructions ###
- [ ] Create application with the following models and fieldnames:
  - [ ] `Dog` model
    - [ ] `name`
    - [ ] `image_filename`
    - [ ] `breed`
    - [ ] `age` (integer for months)
    - [ ] `gender` ('m' for male, 'f' for female, 'u' for unknown)
    - [ ] `size` ('s' small, 'm' medium, 'l' large, 'xl' extra large,
          'u' unknown)
  - [ ] `UserDog` model
    - [ ] `user`
    - [ ] `dog`
    - [ ] `status` ('l' liked, 'd' disliked)
  - [ ] `UserPref` model
    - [ ] `user`
    - [ ] `age` ('b' baby, 'y' young, 'a' adult, 's' senior)
    - [ ] `gender` ('m' male, 'f' female)
    - [ ] `size` ('s' small, 'm' medium, 'l' large, 'xl' extra large)
- [ ] Create serializers:
  - [ ] `Dog` (all fields need to be revealed)
  - [ ] `UserPref` (all fields need to be revealed except `user`)
- [ ] Create routes:
  - [ ] get dogs:
    - [ ] next liked: `/api/dog/<pk>/liked/next/`
    - [ ] next disliked: `/api/dog/<pk>/disliked/next/`
    - [ ] next undecided: `/api/dog/<pk>/undecided/next/`
  - [ ] set dog's status:
    - [ ] like: `/api/dog/<pk>/liked/`
    - [ ] dislike: `/api/dog/<pk>/disliked/`
    - [ ] undecided: `/api/dog/<pk>/undecided/`
  - [ ] set user preferences:
    - [ ] `/api/user/preferences/`
- [ ] The supplied project uses Token-based Auth. This functionality should be
      maintained.
- [ ] Unit Tests
- [ ] Allow addition/deletion of dogs to the site
- [ ] Add additional data fields to the models to increase app functionality
- [ ] Add additional routes to the site to increase functionality
- [ ] >75% Test coverage

### vs Specs from How You Will Be Graded ###
12345678901234567890123456789012345678901234567890123456789012345678901234567890
- [ ] Script runs correctly
- [ ] Correct dogs are shown
- [ ] Ability to add/remove dogs
- [ ] `Dog` Model:
  - [ ] Properly configured
  - [ ] `name`
  - [ ] `image_filename`
  - [ ] `breed`
  - [ ] `age` (integer months)
  - [ ] `gender` ('m'/'f'/'u')
  - [ ] `size` ('s'/'m'/'l'/'xl')
  - [ ] Other relevant fields to increase functionality
- [ ] `UserDog` Model:
  - [ ] Properly configured
  - [ ] `user`
  - [ ] `dog`
  - [ ] `status` ('l'/'d')
  - [ ] Other relevant fields to increase functionality
- [ ] `UserPref` Model:
  - [ ] Properly configured
  - [ ] `user`
  - [ ] `age` ('b'/'y'/'a'/'s')
  - [ ] `gender` ('m'/'f')
  - [ ] `size` ('s'/'m'/'l'/'xl')
  - [ ] Other relevant fields to increase functionality
- [ ] `Dog` serializer
  - [ ] reveals all fields
- [ ] `UserPref` serializer
  - [ ] reveals all fields except `user`
- [ ] Routes:
  - [ ] next dog:
    - [ ] next liked: `/api/dog/<pk>/liked/next/`
    - [ ] next disliked: `/api/dog/<pk>/disliked/next/`
    - [ ] next undecided: `/api/dog/<pk>/undecided/next/`
  - [ ] set dog's status:
    - [ ] like: `/api/dog/<pk>/liked/`
    - [ ] dislike: `/api/dog/<pk>/disliked/`
    - [ ] undecided: `/api/dog/<pk>/undecided/`
  - [ ] set user preferences:
    - [ ] `/api/user/preferences/`
  - [ ] additional routes that increase functionality
- [ ] Token-based Auth
- [ ] Unit Tests
  - [ ] >50% coverage
  - [ ] >75% coverage
- [ ] PEP8 Compliant
