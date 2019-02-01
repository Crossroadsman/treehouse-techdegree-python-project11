from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        
        fields = ('username', 'password')
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dog
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
        )


class UserPrefSerializer(serializers.ModelSerializer):
    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE)
    age = CharField(max_length=1, choices=AGE_CHOICES)
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=2, choices=SIZE_CHOICES)

    class Meta:
        model = models.UserPref
        fields = (
            'id',
            ### TODO: REMOVE THIS WHEN DONE TESTING ###
            'user'
            ### TODO: REMOVE THIS WHEN DONE TESTING ###
            'age',
            'gender',
            'size',
        )
