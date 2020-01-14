import logging

from .base import VALID_DOG_DATA, PugOrUghTestCase

from pugorugh.forms import AddDogForm
from pugorugh.models import Dog


class AddDogFormTestCase(PugOrUghTestCase):

    # setUp and tearDown
    # ------------------
    def setUp(self):

        self.initial_dog_data = VALID_DOG_DATA[:2]
        self.create_some_dogs(self.initial_dog_data)

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
