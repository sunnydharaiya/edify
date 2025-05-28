from django.contrib import admin
from .models import GrammarCategory, GrammarActivity, GrammarQuestion, GrammarOption,DragDropActivity, DragDropType, DragDropWord,PickWordsActivity, PickWordsSentence, PickWordsWord


class GrammarOptionInline(admin.TabularInline):
    model = GrammarOption
    extra = 1  # Add one extra empty option row by default
    fields = ('option_text', 'is_correct')  # Fields to display for each option

class GrammarQuestionInline(admin.TabularInline):
    model = GrammarQuestion
    extra = 1  # Add one extra empty question row by default
    inlines = [GrammarOptionInline]  # This will show options inline with questions
    fields = ('question', 'image')  # Display question text and image

@admin.register(GrammarCategory)
class GrammarCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category__name')
    list_filter = ('category',)

@admin.register(GrammarActivity)
class GrammarActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    inlines = [GrammarQuestionInline]  # Show questions inside each activity

@admin.register(GrammarQuestion)
class GrammarQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'activity', 'image')
    search_fields = ('question', 'activity__name')
    inlines = [GrammarOptionInline]

class DragDropWordInline(admin.TabularInline):
    model = DragDropWord
    extra = 1
    fields = ('word',)


@admin.register(DragDropType)
class DragDropTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity')
    search_fields = ('name', 'activity__name')
    inlines = [DragDropWordInline]  # Words will appear inline under DragDropType


@admin.register(DragDropActivity)
class DragDropActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')

class PickWordsWordInline(admin.TabularInline):
    model = PickWordsWord
    extra = 1
    fields = ('word',)

@admin.register(PickWordsSentence)
class PickWordsSentenceAdmin(admin.ModelAdmin):
    list_display = ('sentence', 'activity')
    search_fields = ('sentence', 'activity__name')
    inlines = [PickWordsWordInline]  
    
class PickWordsSentenceInline(admin.TabularInline):
    model = PickWordsSentence
    extra = 1
    fields = ('sentence',)
    inlines = [PickWordsWordInline]  


@admin.register(PickWordsActivity)
class PickWordsActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category__title')
    inlines = [PickWordsSentenceInline]







