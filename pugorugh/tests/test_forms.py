from io import BytesIO
import logging

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image

from pugorugh.forms import AddDogForm
from pugorugh.models import Dog


class AddDogFormTestCase(TestCase):

    # setUp and tearDown
    # ------------------
    def setUp(self):

        self.initial_dog_data = [
            {
                'name': 'lucy',
                'image_filename': 'lucy.jpg',
                'age': 56,
                'gender': 'f',
                'size': 'l',
                'breed': 'labrador retriever'
            },
            {
                'name': 'rosie',
                'image_filename': 'rosie.jpg',
                'age': 24,
                'gender': 'f',
                'size': 'l',
                'breed': 'labrador retriever'
            },
        ]

        for dog in self.initial_dog_data:
            Dog.objects.create(**dog)


    # Helper Methods
    # --------------
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

    # Tests
    # -----

    def test_get_next_pk_correctly_returns_next_pk(self):

        dogs = Dog.objects.all()
        
        test_form = AddDogForm()

        self.assertEqual(
            dogs.count() + 1,
            test_form.get_next_pk()
        )

    def test_form_creates_valid_dog(self):

        # create an image file
        test_image_file = self.make_image_file()
        
        # seek to beginning of file
        test_image_file.seek(0)

        test_data =  {
            'name': 'dougie',
            'age': 13,
            'gender': 'm',
            'size': 'l',
            'breed': 'labrador retriever'
        }
        test_files = {'image': test_image_file}
        
        test_form = AddDogForm(test_data, test_files)

        logging.debug(test_form)

        test_form.is_valid()

        logging.debug(test_form.errors.as_data())

        test_form.save()

        dog = Dog.objects.get(name=test_data['name'])

        for field in [
            'name',
            'age',
            'gender',
            'size',
            'breed'
        ]:
            self.assertEqual(
                getattr(dog, field),
                test_data[field]
            )

        self.assertEqual(
            getattr(dog, 'image_filename'),
            '3.jpg'
        )

