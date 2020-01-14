import os
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from PIL import Image

from pugorugh.models import UserPref, Dog, UserDog


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

VALID_DOG_DATA = [
    {
        'name': 'lucy',
        'image_filename': 'test_image_01.jpg',
        'age': 52,
        'gender': 'f',
        'size': 'l'
    },
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
        'age': 85,
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

VALID_STATUS_LIST = ['l', 'l', 'u', 'u', 'd', 'd']

TEST_DIRECTORY = tempfile.TemporaryDirectory()


@override_settings(DOG_UPLOAD_DIR = os.path.join(TEST_DIRECTORY.name, 'images', 'dogs'))
class PugOrUghTestCase(TestCase):
    
    # Helper Methods
    # --------------
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
            dog = Dog.objects.create(**VALID_DOG_DATA[0])
        return dog

    def create_valid_userdog(self, user, dog, status):
        userdog = UserDog.objects.create(
            user=user,
            dog=dog,
            status=status
        )
        return userdog

    def create_some_dogs(self, dog_data_list):
        for dog_data in dog_data_list:
            self.create_valid_dog(**dog_data)

    def create_some_userdogs(self, user, status_list):
        all_dogs = Dog.objects.all()
        for i, status in enumerate(status_list):
            if status == 'u':  # don't create a userdog
                continue
            self.create_valid_userdog(
                user=user,
                dog=all_dogs[i],
                status=status
            )

    def make_image_data(self):
        """Creates an in-memory byte stream containing image data
        then returns it.
        """
        
        # Create the in-memory binary stream object
        image_data = BytesIO()

        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html
        image_settings = {
            'mode': "RGB",
            'size': (128, 128)
        }
        # `fp` : A filename (string), pathlib.Path object or file object
        # `format` : If None, format is inferred from file extension
        #      (explicitly setting format is required if using a file
        #      object instead of a filename)
        stream_settings = {
            'fp': image_data,
            'format': 'JPEG',

        }
        image_object = Image.new(**image_settings)
        image_object.save(**stream_settings)  # write img data to stream

        return image_data

    def make_image_file(self):
        """Creates an in-memory image file and returns it."""
        image_data = self.make_image_data()

        # Note, when getting the string representation of the file it is
        # described as:
        # `test_file.jpg (text/plain)`
        # It doesn't seem to be an issue that Django thinks it is a text
        # file:
        # Running readlines on the file reveals it to be a binary file
        # And PIL is able to read the file without complaint.
        image_file = SimpleUploadedFile('test_file.jpg', image_data.getvalue())

        return image_file
