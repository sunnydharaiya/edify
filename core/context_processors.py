# core/context_processors.py
from .models import Category
from activity.models import ExpressionGroup
from phonics.models import Phase
from vocabulary.models import GenericActivity
from grammar.models import GrammarCategory

def categories_processor(request):
    categories = Category.objects.filter(reading__isnull=False).distinct().prefetch_related('reading_set')
    return {
        'header_categories': categories
    }


def expression_groups(request):
    return {
        'expression_groups': ExpressionGroup.objects.all()
    }

def phases(request):
    phases = Phase.objects.all()
    return {
        'phases': phases
    }
def activities(request):
    categories = Category.objects.filter(activities__isnull=False).distinct().prefetch_related('activities')
    return {'categories': categories}

def grammar_categories(request):
    categories = Category.objects.filter(grammar_categories__isnull=False).distinct().prefetch_related('grammar_categories')
    return {'gcategories': categories}