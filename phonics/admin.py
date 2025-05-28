from django.contrib import admin
from .models import SoundActivity, Blend, BlendFor, BlendWord, Rhyming, RhymingFor, RhymingWord, TrickyWord, ReadAndListen, AlternativeSpelling, AlternativeSpellingWord, Phase, PhaseFor, PhaseWord, IdentifyWords, IdentifyWordOption, Vowel, VowelWord, VowelsAlphabet, EnglishAlphabet

@admin.register(SoundActivity)
class SoundActivityAdmin(admin.ModelAdmin):
    list_display = ('word', 'category', 'type', 'audio')
    search_fields = ('word', 'category__name')
    list_filter = ('type', 'category')

@admin.register(Blend)
class BlendAdmin(admin.ModelAdmin):
    list_display = ('type', 'category')
    search_fields = ('type', 'category__name')
    list_filter = ('type', 'category')

class BlendWordInline(admin.TabularInline):
    model = BlendWord
    extra = 1


@admin.register(BlendFor)
class BlendForAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type__name')
    list_filter = ('type',)
    inlines = [BlendWordInline]


class RhymingWordInline(admin.TabularInline):
    model = RhymingWord
    extra = 1

class RhymingForInline(admin.TabularInline):
    model = RhymingFor
    extra = 1

@admin.register(Rhyming)
class RhymingAdmin(admin.ModelAdmin):
    list_display = ('type', 'category')

@admin.register(RhymingFor)
class RhymingForAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    inlines = [RhymingWordInline]


@admin.register(TrickyWord)
class TrickyWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'category', 'audio')
    search_fields = ('word', 'category__name')


@admin.register(ReadAndListen)
class ReadAndListenAdmin(admin.ModelAdmin):
    list_display = ('heading', 'category', 'audio')
    search_fields = ('heading', 'category__name')

class AlternativeSpellingWordInline(admin.TabularInline):
    model = AlternativeSpellingWord
    extra = 1
    fields = ('sentence', 'image', 'answer', 'audio')
    readonly_fields = ('audio',)  

@admin.register(AlternativeSpelling)
class AlternativeSpellingAdmin(admin.ModelAdmin):
    list_display = ('type', 'category', 'slug')
    search_fields = ('type', 'category__name')
    readonly_fields = ('slug',)
    inlines = [AlternativeSpellingWordInline]

class PhaseForInline(admin.TabularInline):
    model = PhaseFor
    extra = 1

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('phase', 'category')
    search_fields = ('phase', 'category__name')
    inlines = [PhaseForInline]


class PhaseWordInline(admin.TabularInline):
    model = PhaseWord
    extra = 1
    fields = ('word', 'image', 'audio')
    readonly_fields = ('audio',)

@admin.register(PhaseFor)
class PhaseForAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase')
    search_fields = ('name', 'phase__phase')
    inlines = [PhaseWordInline]

class IdentifyWordOptionInline(admin.TabularInline):
    model = IdentifyWordOption
    extra = 1

@admin.register(IdentifyWords)
class IdentifyWordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'audio')
    search_fields = ('name', 'category__name')
    inlines = [IdentifyWordOptionInline]
class VowelWordInline(admin.TabularInline):
    model = VowelWord
    extra = 1
    fields = ('word', 'image', 'audio')
    readonly_fields = ('audio',)

@admin.register(Vowel)
class VowelAdmin(admin.ModelAdmin):
    list_display = ('type',)
    inlines = [VowelWordInline]

@admin.register(VowelsAlphabet)
class VowelsAlphabetAdmin(admin.ModelAdmin):
    list_display = ('vowel', 'main_type','word')
    search_fields = ('vowel',)
    list_filter = ('main_type',)

@admin.register(EnglishAlphabet)
class EnglishAlphabetAdmin(admin.ModelAdmin):
    list_display = ('letter','word')
    search_fields = ('letter',)

