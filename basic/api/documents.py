from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Website


@registry.register_document
class WebsiteDocument(Document):

    id = fields.TextField()
    content = fields.TextField(attr="get_content_from_storage")

    class Index:
        name = 'websites'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Website

        fields = [
            'name',
            'url',
            'storage_url',
        ]
