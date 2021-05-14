from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Website, Keyword

class WebsiteResource(resources.ModelResource):
    class Meta:
        model = Website
        fields = ('name', 'url',)


class WebsiteAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'url',
        'keywords',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                # 'name',
                'url',
                # 'keywords',
            ),
        }),
    )
    readonly_fields = [
        'id',
    ]
    search_fields = ['name']

    resource_class = WebsiteResource


class KeywordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'name',
            ),
        }),
    )
    readonly_fields = [
        'id',
    ]
    search_fields = ['name']


admin.site.register(Website, WebsiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
