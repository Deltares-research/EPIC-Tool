from rest_framework import serializers

from epic_app.models.models import Group
from epic_app.serializers.program_serializer import SimpleProgramSerializer


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Group'
    """

    programs = SimpleProgramSerializer(many=True, read_only=True)

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Group
        fields = ("url", "id", "name", "area", "programs")
