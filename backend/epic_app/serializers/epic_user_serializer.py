from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from epic_app.models.epic_user import EpicOrganization, EpicUser


class EpicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for 'EpicUser'
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = EpicUser
        fields = (
            "url",
            "id",
            "username",
            "organization",
            "selected_programs",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(EpicUserSerializer, self).create(validated_data)

    def validate(self, attrs):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        # user = EpicUser(**attrs)

        # get the password from the data
        password = attrs.get("password")

        errors = dict()
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=EpicUser)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e_err:
            errors["password"] = list(e_err.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(EpicUserSerializer, self).validate(attrs)

    def update(self, instance: EpicUser, validated_data: dict) -> EpicUser:
        """
        Partial update of the `EpicUser` fields. At this moment only available to update `password`.

        Args:
            instance (EpicUser): `EpicUser` to update.
            validated_data (dict): Dictionary of values valid to be updated.

        Returns:
            EpicUser: Updated instance.
        """
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class EpicOrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for 'EpicOrganization'
    """

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = EpicOrganization
        fields = ("url", "name", "organization_users")
