from elasticsearch_dsl.query import Q, MultiMatch

from .documents import WebsiteDocument


def search(string):
    """
    Sample test search function , returns search object. Will have to for loops through results to see:
    i.e. results = search("avolin")
    for r in results:
        print(r.name)
    """
    search = WebsiteDocument.search()

    q = Q("multi_match", query=string, fields=['name', 'url', 'storage_url'])

    search = search.query(q)

    return search.to_queryset()
