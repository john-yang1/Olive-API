from django.contrib import admin

from .models import Website


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


admin.site.register(Website, WebsiteAdmin)
