from django.contrib import admin
from .models import SpellingGroup, SpellingType, SpellingWord,LongVowelSound,UnscrambleActivity,ExpressionGroup, ExpressionObject, ExpressionOption,VowelWord

admin.site.register(SpellingGroup)
class SpellingWordInline(admin.TabularInline):  # Or use StackableInline if you prefer a different layout
    model = SpellingWord
    extra = 1  # This controls how many empty forms are displayed (set to 1 or more if you want users to add new ones)

class SpellingTypeAdmin(admin.ModelAdmin):
    inlines = [SpellingWordInline]  # This adds SpellingWord inline to SpellingType admin view

admin.site.register(SpellingType, SpellingTypeAdmin)

@admin.register(LongVowelSound)
class LongVowelSoundAdmin(admin.ModelAdmin):
    list_display = ('word', 'category', 'is_correct')
    list_filter = ('category', 'is_correct')
    search_fields = ('word',)

@admin.register(UnscrambleActivity)
class UnscrambleActivityAdmin(admin.ModelAdmin):
    list_display = ('sentence_part_1', 'sentence_part_2', 'scrambled_word', 'category')
    list_filter = ('category',)
    search_fields = ('sentence_part_1', 'sentence_part_2', 'word')

class ExpressionOptionInline(admin.TabularInline):
    model = ExpressionOption
    extra = 1  # Display an extra empty row


class ExpressionObjectInline(admin.TabularInline):
    model = ExpressionObject
    extra = 1  # Display an extra empty row


@admin.register(ExpressionGroup)
class ExpressionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    inlines = [ExpressionObjectInline]


class ExpressionOptionInline(admin.TabularInline):
    model = ExpressionOption
    extra = 1
    fields = ('option_text', 'is_correct')


@admin.register(ExpressionObject)
class ExpressionObjectAdmin(admin.ModelAdmin):
    list_display = ('group', 'display_image', 'display_correct_options')
    search_fields = ('group__name',)
    inlines = [ExpressionOptionInline]

    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="75" height="75"/>'
        return "No Image"
    display_image.allow_tags = True
    display_image.short_description = "Image"

    def display_correct_options(self, obj):
        correct_options = obj.options.filter(is_correct=True)
        return ", ".join([option.option_text for option in correct_options])
    display_correct_options.short_description = "Correct Answers"
    
@admin.register(VowelWord)
class VowelWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'vowel_type', 'audio_file')
    search_fields = ('word',)