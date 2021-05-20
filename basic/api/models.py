import re

from django.core.exceptions import ValidationError
from django.db import models
import uuid
import os

import requests
import boto3
from bs4 import BeautifulSoup
import re

s3_bucket_name = os.getenv('DJANGO_AWS_S3_BUCKET')
access_key_id = os.getenv('DJANG0_AWS_ACCESS_KEY')
secret_access_key = os.getenv('DJANG0_AWS_SECRET_ACCESS_KEY')
region = os.getenv('DJANGO_AWS_REGION')
aws_app = "s3"


def get_all_keywords():
    return [k.name for k in Keyword.objects.all()]


def create_s3_connection():
    try:
        s3 = boto3.resource(aws_app, region_name=region,
                            aws_access_key_id=access_key_id,
                            aws_secret_access_key=secret_access_key)
        print("Connected to S3..")
        return s3
    except Exception as e:
        print("Exception occurred while trying to connect to the AWS S3 bucket: " + e)


def create_s3_client():
    try:
        s3_client = boto3.client(aws_app, region_name=region,
                                 aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_access_key)
        print("Created S3 Client")
        return s3_client
    except Exception as e:
        print("Exception occurred trying to create s3 client connection: " + e)


def create_presigned_url(object_name, expiration=31540000):  # Default expiration time to 1 year
    s3 = create_s3_client()
    try:
        response = s3.generate_presigned_url('get_object', Params={'Bucket': os.getenv('DJANGO_AWS_S3_BUCKET'),
                                                                   'Key': object_name}, ExpiresIn=expiration)
        return response
    except Exception as e:
        print("Exception occurred creating presigned url" + e)


class Website(models.Model):
    """Website keyword."""

    # Fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        blank=True,
    )
    url = models.URLField(
        max_length=255,
        blank=True,
        unique=True
    )
    keywords = models.JSONField(
        null=True,
        blank=True
    )
    storage_url = models.URLField(
        max_length=255,
        blank=True
    )  # Url link to s3 object, can call requests.get(self.storage_url) to get file(html data)

    def get_content_from_storage(self):
        """
        Gets content (html text) from storage url and returns it. Used by WebsiteDocument to get stored as content field
        """
        r = requests.get(self.storage_url, verify=True)
        return r.text

    def get_company_name_from_url(self):
        try:
            stripped_url = re.findall(
                r'(?<=\.)([^.]+)(?:\.(?:co\.uk|co\.in|co\.nz|co\.ke|co\.za|ac\.us|[^.]+(?:$|\n)))',
                self.url)
            company_name = stripped_url[0]
            print('Company name: {}'.format(company_name))
            return company_name
        except Exception as e:
            print(e)

    def get_website_keyword_frequency_json(self, html):
        try:
            keyword_frequency_count_for_site = {}
            parsing_html = BeautifulSoup(html, 'html.parser')
            all_keywords = get_all_keywords()
            for keyword in all_keywords:
                all_matches = parsing_html.find_all(text=re.compile(keyword, re.IGNORECASE))
                for match in all_matches:
                    print(f"keyword: {keyword}, word found: {match}")
                keyword_frequency_count_for_site[keyword] = len(all_matches)
            return keyword_frequency_count_for_site
        except Exception as e:
            print(e)

    def get_website_storage_url(self):
        try:
            print("Generating storage url")
            s3_object = f"{'__'.join(self.url.split('/')[2:])}.html"
            url = create_presigned_url(s3_object)
            print("Created presigned url: " + url)
            return url
        except Exception as e:
            print(e)

    def save_url_to_s3_and_return_html(self):
        s3 = create_s3_connection()
        r = requests.get(self.url, verify=True)
        s3.Object(s3_bucket_name, f"{'__'.join(self.url.split('/')[2:])}.html").put(Body=r.text)
        print(f"Saved {self.url} to S3..")
        return r.text

    def save(self, **kwargs):

        raw_html = self.save_url_to_s3_and_return_html()
        storage_location_url = self.get_website_storage_url()
        website_name = self.get_company_name_from_url()
        keyword_frequency_count_json = self.get_website_keyword_frequency_json(raw_html)

        self.keywords = keyword_frequency_count_json
        self.name = website_name
        self.storage_url = storage_location_url

        print(f"extracted company name: {self.name}")
        print(f"storage url: {self.storage_url}")

        super().save(**kwargs)

        # update ES record with raw HTML
        # TODO



    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['name']


class Keyword(models.Model):
    """Keywords."""

    # Fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def update_existing_websites(self):
        print('Updating existing websites with newly added keywords..')
        # Retrieve all website html pages from S3

    def scrape(self):
        print('Scraping {}'.format(self.name))

    def save(self, **kwargs):
        self.scrape()

        super().save(**kwargs)

    # Magic
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['name']
