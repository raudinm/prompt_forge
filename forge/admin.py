from django.contrib import admin
from .models import Prompt, PromptMetadata

# Register your models here.


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'created_at']
    ordering = ['-created_at']
    search_fields = ['text', 'response', 'user__username']
    list_filter = ['created_at', 'user']


@admin.register(PromptMetadata)
class PromptMetadataAdmin(admin.ModelAdmin):
    list_display = ['id', 'prompt', 'model_used', 'sent_via_websocket']
    ordering = ['-prompt__created_at']
    search_fields = ['model_used', 'prompt__text']
    list_filter = ['model_used', 'sent_via_websocket']
