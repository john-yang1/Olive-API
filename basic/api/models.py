from django.core.exceptions import ValidationError
from django.db import models
import uuid

import os

import requests
import boto3

s3_bucket_name = os.getenv('DJANGO_AWS_S3_BUCKET')
access_key_id = os.getenv('DJANG0_AWS_ACCESS_KEY')
secret_access_key = os.getenv('DJANG0_AWS_SECRET_ACCESS_KEY')
region = os.getenv('DJANGO_AWS_REGION')
aws_app = "s3"


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
        unique=True
    )
    url = models.URLField(
        max_length=255,
        blank=True
    )

    # Instance methods
    def clean(self):
        """Validate requirement-stakeholders project reference match."""
        if self.name == 'ATB':
            raise ValidationError({
                'name': 'Name cannot be ATB',
            })

    def create_s3_connection(self):
        try:
            s3 = boto3.resource(aws_app, region_name=region,
                                aws_access_key_id=access_key_id,
                                aws_secret_access_key=secret_access_key)
            print("Connected to S3..")
            return s3
        except Exception as e:
            print("Exception occurred while trying to connect to the AWS S3 bucket: " + e)

    def scrape(self):
        print('Scraping {}'.format(self.name))
        try:
            s3 = self.create_s3_connection()
            r = requests.get(self.url, verify=True)
            s3.Object(
                s3_bucket_name, f"{'__'.join(self.url.split('/')[2:])}.html").put(Body=r.text)
            print(f"Saved {self.url} to S3..")
        except Exception as e:
            print(e)

    def save(self, **kwargs):
        self.clean()
        self.scrape()

        super().save(**kwargs)

    # Magic
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

    # Instance methods
    def clean(self):
        """Validate requirement-stakeholders project reference match."""
        if self.name == 'ATB':
            raise ValidationError({
                'name': 'Name cannot be ATB',
            })

    def scrape(self):
        print('Scraping {}'.format(self.name))

    def save(self, **kwargs):
        self.clean()
        self.scrape()

        super().save(**kwargs)

    # Magic
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['name']
