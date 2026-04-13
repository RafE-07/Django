from django.contrib import admin
from .models import Mediafile



@admin.register(Mediafile)
class MediafileAdmin(admin.ModelAdmin):
    list_display = ('title','uploaded_at')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)    