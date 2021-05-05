from rest_framework import serializers

from .models import Website


class CreateWebsiteSerializer(serializers.ModelSerializer):
    """Create Website serializer."""

    def validate(self, attrs):
        name = attrs.get('name', None)

        if name == 'ATB':
            raise serializers.ValidationError({
                'name': 'Name cannot be ATB',
            })

        return attrs

    class Meta:
        model = Website
        fields = [
            'name',
            'url',
        ]


class WebsiteSerializer(serializers.ModelSerializer):
    """Base Website serializer."""

    class Meta:
        model = Website
        fields = [
            'id',
            'name',
            'url',
        ]
        read_only_fields = ['id']
