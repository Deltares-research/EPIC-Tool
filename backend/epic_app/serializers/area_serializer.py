from rest_framework import serializers

from epic_app.models.models import Area
from epic_app.serializers.group_serializer import GroupSerializer


class AreaSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Area'
    """

    groups = GroupSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """
        Overriden meta class for serializing purposes.
        """

        model = Area
        fields = ("url", "id", "name", "groups")
