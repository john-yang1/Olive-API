import uuid

from django.db import models
from django.core.exceptions import ValidationError


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
