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
        unique=True,
    )
    url = models.URLField(
        max_length=255,
        blank=True
    )
    keywords = models.JSONField(
        null=True,
        blank=True
    )

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

    def get_website_keyword_frequency_json(self):
        try:
            keyword_frequency_count_for_site = {}
            raw_html = self.save_url_to_s3_and_return_html()
            parsing_html = BeautifulSoup(raw_html, 'html.parser')
            all_keywords = get_all_keywords()
            for keyword in all_keywords:
                all_matches = parsing_html.find_all(text=re.compile(keyword, re.IGNORECASE))
                keyword_frequency_count_for_site[keyword] = len(all_matches)
            return keyword_frequency_count_for_site
        except Exception as e:
            print(e)

    def save_url_to_s3_and_return_html(self):
        s3 = create_s3_connection()
        r = requests.get(self.url, verify=True)
        s3.Object(s3_bucket_name, f"{'__'.join(self.url.split('/')[2:])}.html").put(Body=r.text)
        print(f"Saved {self.url} to S3..")
        return r.text

    def save(self, **kwargs):
        website_name = self.get_company_name_from_url()
        keyword_frequency_count_json = self.get_website_keyword_frequency_json()
        self.keywords = keyword_frequency_count_json
        self.name = website_name
        print(f"extracted company name: {self.name}")
        super().save(**kwargs)

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
