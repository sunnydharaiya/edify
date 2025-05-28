from django.contrib import admin
from .models import Transcript,Reading,TrueFalseActivity,MatchingPair
# Register your models here.
class TranscriptInline(admin.TabularInline):
    model = Transcript
    fields = ('text', 'slug', 'audio_file')
    extra = 1

class MatchingPairInline(admin.TabularInline):
    model = MatchingPair
    fields = ('question', 'response')
    extra = 2
class TrueFalseInline(admin.TabularInline):
    model = TrueFalseActivity
    fields = ('statement', 'is_true')
    extra = 1

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TranscriptInline, TrueFalseInline,MatchingPairInline]
