from rest_framework import viewsets

from .models import Website, Keyword, Potatoe
from .serializers import (
    WebsiteSerializer,
    CreateWebsiteSerializer,
    KeywordSerializer,
    CreateKeywordSerializer,
    CreatePotatoeSerializer,
    PotatoeSerializer
)


class WebsiteViewSet(viewsets.ModelViewSet):
    """Website library ViewSet."""

    search_fields = ['name']
    queryset = Website.objects.all()

    def get_queryset(self):
        model = Website

        return model.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            serializer = CreateWebsiteSerializer
        else:
            serializer = WebsiteSerializer

        return serializer


class KeywordViewSet(viewsets.ModelViewSet):
    """Website library ViewSet."""

    search_fields = ['name']
    queryset = Keyword.objects.all()

    def get_queryset(self):
        model = Keyword

        return model.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            serializer = CreateKeywordSerializer
        else:
            serializer = KeywordSerializer

        return serializer

class PotatoeViewSet(viewsets.ModelViewSet):
    """api potatoe ViewSet."""

    search_fields = ['name']
    queryset = Potatoe.objects.all()

    def get_queryset(self):
        model = Potatoe

        return model.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            serializer = CreatePotatoeSerializer
        else:
            serializer = PotatoeSerializer

        return serializer