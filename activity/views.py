from django.shortcuts import render
from .models import SpellingGroup,LongVowelSound,UnscrambleActivity,ExpressionGroup,ExpressionObject,ExpressionOption,VowelWord
def spelling_drag_drop(request):
    spelling_groups = SpellingGroup.objects.prefetch_related('spelling_types__words').all()
    return render(request, 'activity/spelling_drag_drop.html', {
        'spelling_groups': spelling_groups,
    })

def long_vowel_sound(request):
    long_vowel_sounds = LongVowelSound.objects.all()
    return render(request, 'activity/long_vowel_sound.html', {
        'long_vowel_sounds': long_vowel_sounds,
    })
        
def unscramble_activity(request):
    unscramble_activities = UnscrambleActivity.objects.all()
    return render(request, 'activity/unscramble_activity.html', {
        'unscramble_activities': unscramble_activities,
    })

def expression_group_detail(request, slug):
    expression_group = ExpressionGroup.objects.get(slug=slug)
    return render(request, 'activity/expression_group_detail.html', {
        'expression_group': expression_group,
    })

def vowel_word(request):
    vowel_words = VowelWord.objects.all()
    return render(request, 'activity/vowel_word.html', {
        'vowel_words': vowel_words,
    })
