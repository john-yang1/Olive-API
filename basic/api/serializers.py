from rest_framework import serializers

from .models import Website, Keyword


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


class CreateKeywordSerializer(serializers.ModelSerializer):
    """Create Keyword serializer."""

    def validate(self, attrs):
        name = attrs.get('name', None)

        if name == 'ATB':
            raise serializers.ValidationError({
                'name': 'Name cannot be ATB',
            })

        return attrs

    class Meta:
        model = Keyword
        fields = [
            'name',
            'url',
        ]


class KeywordSerializer(serializers.ModelSerializer):
    """Base Keyword serializer."""

    class Meta:
        model = Keyword
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']


class WebsiteSerializer(serializers.ModelSerializer):
    """Base Website serializer."""

    class Meta:
        model = Website
        fields = [
            'id',
            'name',
            'url',
            'keywords',
            'storage_url',
        ]
        read_only_fields = ['id']

class CreatePotatoeSerializer(serializers.ModelSerializer):
    """Create Keyword serializer."""

    def validate(self, attrs):
        name = attrs.get('name', None)

        if name == 'ATB':
            raise serializers.ValidationError({
                'name': 'Name cannot be ATB',
            })

        return attrs
        
    class Meta:
        model = Keyword
        fields = [
            'name',
            'url',
        ]


class PotatoeSerializer(serializers.ModelSerializer):
    """Base Keyword serializer."""

    class Meta:
        model = Keyword
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']