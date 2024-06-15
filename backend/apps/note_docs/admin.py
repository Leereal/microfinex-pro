from django.contrib import admin
from .models import NoteDoc

class NoteDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_path', 'created_at', 'deleted_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'deleted_at')

admin.site.register(NoteDoc, NoteDocAdmin)
