from django import forms

from .models import Dog


class AddDogForm(forms.ModelForm):

    class Meta:
        model = Dog
        fields = (
            'name',
            'image_filename',  # Need to override this to create the image file
            'age',
            'gender',
            'size',
            'breed',
        )
