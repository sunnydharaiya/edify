from django.shortcuts import render, get_object_or_404
from .models import GrammarCategory, GrammarActivity,DragDropActivity,PickWordsActivity
from core.models import Category




def gramamr_activity_list(request, category_slug, activity_slug):
    # Get parent Category first
    parent_category = get_object_or_404(Category, slug=category_slug)
    
    # Find GrammarCategory linked to parent Category and matching title (or slug)
    category = get_object_or_404(
        GrammarCategory,
        category=parent_category,
        title__iexact=activity_slug.replace('-', ' ')
    )
    
    # Get activities under that GrammarCategory
    activities = GrammarActivity.objects.filter(category=category)
    draganddrop = DragDropActivity.objects.filter(category=category)
    pick = PickWordsActivity.objects.filter(category=category)

    return render(request, 'grammar/gramamr_activity_list.html', {
        'category': category,
        'activities': activities,
        'draganddrop': draganddrop,
        'pick':pick,
    })

def grammar_activity_detail(request, category_slug, activity_name):
    grammar_category = get_object_or_404(GrammarCategory, slug=category_slug)

    activity = get_object_or_404(
        GrammarActivity,
        category=grammar_category,
        name__iexact=activity_name.replace('-', ' ')
    )
    
    questions = activity.questions.prefetch_related('options')

    return render(request, 'grammar/grammar_activity_detail.html', {
        'activity': activity,
        'category': grammar_category,
        'questions': questions,
    })
def dragdrop_activity_detail(request, activity_slug):
    activity = get_object_or_404(DragDropActivity, slug=activity_slug)
    types = activity.dragdroptype_set.prefetch_related('words')
    return render(request, 'grammar/dragdrop_activity_detail.html', {
        'activity': activity,
        'types': types,
    })

def pick_words_activity_detail(request, category_slug, activity_slug):
    category = GrammarCategory.objects.get(slug=category_slug)
    activity = PickWordsActivity.objects.get(category=category, title__iexact=activity_slug.replace('-', ' '))
    sentences = activity.sentences.all().prefetch_related('words')
    
    return render(request, 'grammar/pick_words_activity_detail.html', {
        'category': category,
        'activity': activity,
        'sentences': sentences,
    })