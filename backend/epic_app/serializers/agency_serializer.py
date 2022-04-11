from rest_framework import serializers

from epic_app.models.models import Agency
from epic_app.serializers.program_serializer import SimpleProgramSerializer


class AgencySerializer(serializers.ModelSerializer):
    """
    Serializer for 'Agency'
    """

    programs = SimpleProgramSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Agency
        fields = ("url", "id", "name", "programs")
