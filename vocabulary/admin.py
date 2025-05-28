from django.contrib import admin
from .models import MissingWord, OptionAnswer, GenericActivity, IdentifyPicture, ImageMatchingActivity, ImageWordPair, SynonymAntonymActivity, WordPair, PrefixSuffixActivity, PrefixSuffixWord, PrefixSuffixOption, UnscrambleActivity, UnscrambleEntry

@admin.register(MissingWord)
class MissingWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'activity', 'image')
    search_fields = ('word', 'activity__title')
    list_filter = ('activity',)

class OptionAnswerInline(admin.TabularInline):
    model = OptionAnswer
    extra = 1
    fields = ('option_text', 'is_correct')
    verbose_name = "Option"
    verbose_name_plural = "Options"


@admin.register(GenericActivity)
class GenericActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category')
    list_filter = ('category',)


@admin.register(IdentifyPicture)
class IdentifyPictureAdmin(admin.ModelAdmin):
    list_display = ('activity', 'image', 'category_name')
    search_fields = ('activity__title',)

    def category_name(self, obj):
        return obj.activity.category.name
    category_name.short_description = 'Category'
    inlines = [OptionAnswerInline]  # Now it works correctly

class ImageWordPairInline(admin.TabularInline):
    model = ImageWordPair
    extra = 1
    fields = ('image_1', 'word_1', 'image_2', 'word_2')

@admin.register(ImageMatchingActivity)
class ImageMatchingActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity')
    search_fields = ('title', 'activity__name')
    inlines = [ImageWordPairInline]
class WordPairInline(admin.TabularInline):
    model = WordPair
    extra = 1
    fields = ('main_word', 'synonym', 'antonym')


@admin.register(SynonymAntonymActivity)
class SynonymAntonymActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity')
    search_fields = ('title', 'activity__name')
    inlines = [WordPairInline]

class OptionInline(admin.TabularInline):
    model = PrefixSuffixOption
    extra = 2
    fields = ('option_text', 'is_answer')

class WordInline(admin.TabularInline):
    model = PrefixSuffixWord
    extra = 1
    fields = ('word_text',)
    inlines = [OptionInline]  # This won't work directly in Django, so we handle option inline differently.

# Since Django admin doesn’t support nested inlines out of the box,
# We'll manage Option inline inside WordAdmin separately, and use WordInline only in ActivityAdmin.

@admin.register(PrefixSuffixWord)
class PrefixSuffixWordAdmin(admin.ModelAdmin):
    list_display = ('word_text', 'prefix_suffix_activity')
    inlines = [OptionInline]

@admin.register(PrefixSuffixActivity)
class PrefixSuffixActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'activity')
    list_filter = ('type', 'activity')
    search_fields = ('title',)
    inlines = [WordInline]

class UnscrambleEntryInline(admin.TabularInline):
    model = UnscrambleEntry
    extra = 1

@admin.register(UnscrambleActivity)
class UnscrambleActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'type')
    list_filter = ('activity', 'type')
    inlines = [UnscrambleEntryInline]

