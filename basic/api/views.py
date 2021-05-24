from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from .models import Website, Keyword
from .serializers import (
    WebsiteSerializer,
    CreateWebsiteSerializer,
    KeywordSerializer,
    CreateKeywordSerializer,
)
from .utils import search
from django.http import HttpResponse
from django.http.response import JsonResponse

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

    @action(methods=['get'],
            detail=False,
            url_path='search',
            suffix='Search')
    def search(self, request):

        query = request.query_params.get('search', None)

        if not query:
            return Response(status=status.HTTP_204_NO_CONTENT)

        queryset = search(query)

        serializer = WebsiteSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = WebsiteSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        keyword = Website.objects.get(name=request.data['name'])
        if keyword:
            keyword.delete()
            return Response({'message': 'Website was deleted successfully!'})
        return Response({'message': 'Delete Failed'})


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

    def post(self, request, *args, **kwargs):
        serializer = KeywordSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        keyword = Keyword.objects.get(name=request.data['name'])
        if keyword:
            keyword.delete()
            return Response({'message': 'Keyword was deleted successfully!'})
        return Response({'message': 'Delete Failed'})