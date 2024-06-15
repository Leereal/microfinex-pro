from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'loan', 'transaction', 'content', 'user', 'created_at', 'deleted_at')
    list_filter = ('client', 'loan', 'transaction', 'user', 'created_at', 'deleted_at')
    search_fields = ('client__name', 'loan__id', 'transaction__id', 'user__username')
    readonly_fields = ('created_at', 'deleted_at')

admin.site.register(Note, NoteAdmin)
