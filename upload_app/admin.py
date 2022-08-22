from django.contrib import admin
from .models import Database, SliceBase


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'database', 'published')
    list_display_links = ('title', 'database')
    search_fields = ('title', 'database')


admin.site.register(Database, DatabaseAdmin)


class SliceBaseAdmin(admin.ModelAdmin):
    list_display = ('db_parent', 'title', 'json_db', 'filter', 'sorting', 'published')

admin.site.register(SliceBase, SliceBaseAdmin)



