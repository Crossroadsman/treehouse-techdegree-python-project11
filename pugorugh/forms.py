from PIL import Image

from django import forms

from .models import Dog
from . import file_handling


class AddDogForm(forms.ModelForm):

    # We are explicitly instantiating the image form field (so that we can
    # get an image file from the user then turn it into a charfield to 
    # maintain compatibility with the existing app).
    # Because we are defining it here, we won't get the benefit of Django's
    # automatic model field validation, so we need to manually specify the
    # validator
    # see:
    # https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#overriding-the-default-fields
    image = forms.ImageField(
        max_length=255
    )

    class Meta:
        model = Dog
        fields = (
            'name',
            # 'image_filename',  # Need to override this to create the image file
            'age',
            'gender',
            'size',
            'breed',
        )

    # The ModelForm's save() method creates and saves the database object.
    # Therefore we can create the new dog model (with a null value for the 
    # filename), get its pk, then call the file handling code to produce a 
    # filename, then put that in the model and save it.
    # see: 
    # https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#the-save-method
    def save(self, commit=True):
        self.image_filename = ""  # image_filename is a required field
        dog = super().save(commit=False)

        # pk is provided by the DB not by Django so it is impossible to
        # get the actual PK before we persist the object to the database.
        # Thus we guess what the next pk will be
        pk = self.get_next_pk()

        image_file = self.cleaned_data.get('image')
        dog.image_filename = file_handling.process_upload(image_file, pk)

        if commit:
            dog.save()
        return dog

    def get_next_pk(self):
        """This only works because we've explicitly made `pk` our "order by"
        property on the model.
        """
        return Dog.objects.last().pk + 1

