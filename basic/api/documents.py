from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Website
from elasticsearch_dsl.query import Q, MultiMatch


@registry.register_document
class WebsiteDocument(Document):
    class Index:
        name = 'websites'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Website

        fields = [
            'name',
            'url',
            'storage_url',
        ]


def search(name):
    """
    Sample test search function , returns search object. Will have to for loops through results to see:
    i.e. results = search("avolin")
    for r in results:
        print(r.name)
    """
    search = WebsiteDocument.search()
    q = Q("multi_match", query=name, fields=['name', 'url', 'storage_url'])
    search = search.query(q)
    return search
