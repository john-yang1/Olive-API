from django.contrib import admin

from .models import Website, Keyword


class WebsiteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'url',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'name',
                'url',
            ),
        }),
    )
    readonly_fields = [
        'id',
    ]
    search_fields = ['name']


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