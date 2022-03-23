from multiprocessing import context
from typing import Optional
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from epic_app.models import EpicUser, Question, Answer

class EpicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for 'EpicUser'
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=EpicUser
        fields = ('url', 'id', 'username', 'organization', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(EpicUserSerializer, self).create(validated_data)

    def validate(self, attrs):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        # user = EpicUser(**attrs)

        # get the password from the data
        password = attrs.get('password')

        errors = dict() 
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=EpicUser)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e_err:
            errors['password'] = list(e_err.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(EpicUserSerializer, self).validate(attrs)

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Question'
    """
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=Question
        fields=('url', 'id', 'description', )

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for 'QuestionAnswerForm'
    """
    
    class Meta:
        """
        Overriden meta class for serializing purposes.
        """
        model=Answer
        fields=('url', 'id', 'user', 'question', 'short_answer', 'long_answer')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        def get_user_query_set():
            current_user = self.context['request'].user
            if current_user.is_staff or current_user.is_superuser:
                return EpicUser.objects.all()
            else:
                return EpicUser.objects.all().filter(id=current_user.id)
        self.fields['user'] = serializers.PrimaryKeyRelatedField(queryset=get_user_query_set())