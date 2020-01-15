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

        # create associated UserPref object
        models.UserPref.objects.create(user=user)

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
            'favourite_toy',
            'favourite_treat',
        )


# A serializer's `save` method will either create a new instance or update
# an existing instance, depending on whether an existing instance was
# passed when instantiating the serializer.
#
# You can pass additional attributes to save() (e.g., the current user):
# ```python
# serializer.save(owner=request.user)
# ```
#
# Any additional kwargs will be included in the validated_data arg when
# .create or .update are called
#
# You can also pass context info to the serializer on instantiation:
# serializer = serializers.UserPrefSerializer(
#     data=request_data, context={'user': user}
# )
class UserPrefSerializer(serializers.ModelSerializer):

    # Custom Field-Level Validation
    # -----------------------------
    def validate_age(self, value):
        valid_ages = ['b', 'y', 'a', 's']
        age_components = value.split(",")
        for age in age_components:
            if age not in valid_ages:
                raise serializers.ValidationError("Invalid character in ages")
        age_set = set(age_components)
        if len(age_components) != len(age_set):
            raise serializers.ValidationError("Repeated character in ages")
        return value

    def validate_gender(self, value):
        valid_genders = ['m', 'f']
        gender_components = value.split(",")
        for gender in gender_components:
            if gender not in valid_genders:
                raise serializers.ValidationError("Invalid char. in genders")
        gender_set = set(gender_components)
        if len(gender_components) != len(gender_set):
            raise serializers.ValidationError("Repeated character in genders")
        return value

    def validate_size(self, value):
        valid_sizes = ['s', 'm', 'l', 'xl']
        size_components = value.split(",")
        for size in size_components:
            if size not in valid_sizes:
                raise serializers.ValidationError("Invalid character in sizes")
        size_set = set(size_components)
        if len(size_components) != len(size_set):
            raise serializers.ValidationError("Repeated character in sizes")
        return value

    def create(self, validated_data):
        # see https://www.django-rest-framework.org/api-guide/validators/
        # #advanced-field-defaults
        # "request must have been provided as part of the context dictionary
        # when instantiating the serializer"
        # pass user into save -> it comes through as an element in
        # validated_data
        return models.UserPref.objects.create(**validated_data)

    def update(self, instance, validated_data):

        # a user can't change another user's user association
        instance.user = instance.user

        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance

    class Meta:
        model = models.UserPref
        fields = (
            'age',
            'gender',
            'size',
            'breed',
            'favourite_toy',
            'favourite_treat',
        )
