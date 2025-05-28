from django.shortcuts import render
from phonics.models import Vowel, VowelWord, VowelsAlphabet ,SoundActivity,Blend,BlendFor,Rhyming,RhymingFor,RhymingWord,TrickyWord,Phase,PhaseFor,PhaseWord,ReadAndListen  
from phonics.models import AlternativeSpelling,AlternativeSpellingWord,IdentifyWords,IdentifyWordOption,EnglishAlphabet
from collections import defaultdict
from core.models import Category
import random
from string import ascii_uppercase
from django.shortcuts import get_object_or_404
# Create your views here.
def vowel_word_list(request, type):
    vowels = Vowel.objects.filter(type=type).prefetch_related('vowel_words')
    vowel_word_list = VowelWord.objects.filter(vowel__type=type)
    

    return render(request, 'phonics/vowel_word_list.html', {
        'vowels': vowels,
        'type': type,
        'vowel_word_list': vowel_word_list,
    })

def sound_activity_list(request, position, level):
    activities = SoundActivity.objects.filter(category__name__iexact=level, type=position)

    activity_options = []
    for activity in activities:
        # Find the correct letter to hide based on the position type
        if position == 'beginning':
            hidden_letter = activity.word[0].upper()
            index_to_hide = 0
        elif position == 'middle':
            index_to_hide = len(activity.word) // 2
            hidden_letter = activity.word[index_to_hide].upper()
        elif position == 'ending':
            index_to_hide = len(activity.word) - 1
            hidden_letter = activity.word[index_to_hide].upper()
        else:
            hidden_letter = ''  # Fallback

        # Get 4 random incorrect letters excluding the hidden letter
        incorrect_letters = list(set(ascii_uppercase) - set(hidden_letter))
        chosen_incorrect = random.sample(incorrect_letters, 4)

        # Combine and shuffle options
        options = chosen_incorrect + [hidden_letter]
        random.shuffle(options)

        # Append to activity options
        activity_options.append({
            'activity': activity,
            'hidden_letter': hidden_letter,
            'options': options,
        })

    return render(request, 'phonics/sound_activity_list.html', {
        'activity_options': activity_options,
        'position': position,
        'level': level,
    })

def blend_list(request, level):
    blends = Blend.objects.filter(category__name__iexact=level)
    return render(request, 'phonics/blend_list.html', {
        'blends': blends,
        'level': level,
    })

def blend_for_list(request, blend_id):
    blend = get_object_or_404(Blend, id=blend_id)
    blend_fors = BlendFor.objects.filter(type=blend).prefetch_related('blend_words')

    blend_data = []
    for blend_for in blend_fors:
        words = list(blend_for.blend_words.all())  # Convert to list to shuffle
        random.shuffle(words)  # Shuffle the list
        blend_data.append({
            'blend_for': blend_for,
            'words': words
        })

    return render(request, 'phonics/blend_for_list.html', {
        'blend': blend,
        'blend_data': blend_data,
    })

def rhyming_list(request, level):
    rhyming = Rhyming.objects.filter(category__name__iexact=level)
    rhyming_for = RhymingFor.objects.filter(type__in=rhyming)
    rhyming_words = RhymingWord.objects.filter(rhyming_for__type__category__name__iexact=level)
    
    return render(request, 'phonics/rhyming_list.html', {
        'rhyming': rhyming,
        'rhyming_for': rhyming_for,
        'rhyming_words': rhyming_words,
        'level': level,
    })

def tricky_word_list(request, level):
    tricky_words = TrickyWord.objects.filter(category__name__iexact=level)
    return render(request, 'phonics/tricky_word_list.html', {
        'tricky_words': tricky_words,
        'level': level,
    })

def phase_view(request, phase):
    phase = get_object_or_404(Phase, phase=phase)
    phase_fors = PhaseFor.objects.filter(phase=phase)
    phase_words = PhaseWord.objects.filter(phase_for__in=phase_fors)
    return render(request, 'phonics/phase_view.html', {
        'phase': phase,
        'phase_fors': phase_fors,
        'phase_words': phase_words,
    })

def read_listen_list(request, level):
    read_listen = ReadAndListen.objects.filter(category__name__iexact=level)
    return render(request, 'phonics/read_listen_list.html', {
        'read_listen': read_listen,
        'level': level,
    })

def alternative_spelling_list(request, level):
    alternative_spelling = AlternativeSpelling.objects.filter(category__name__iexact=level)
    return render(request, 'phonics/alternative_spelling_list.html', {
        'alternative_spelling': alternative_spelling,
        'level': level,
    })

def alternative_spelling_detail(request, slug):
    alternative_spelling = get_object_or_404(AlternativeSpelling, slug=slug)
    alternative_spelling_words = AlternativeSpellingWord.objects.filter(alternative_spelling=alternative_spelling)
    return render(request, 'phonics/alternative_spelling_detail.html', {
        'alternative_spelling': alternative_spelling,
        'alternative_spelling_words': alternative_spelling_words,
    })

def identify_words_list(request, level):
    identify_words = IdentifyWords.objects.filter(category__name__iexact=level)
    indentidy_options = IdentifyWordOption.objects.filter(identify_word__in=identify_words)
    return render(request, 'phonics/identify_words_list.html', {
        'identify_words': identify_words,
        'indentidy_options': indentidy_options,
        'level': level,
    })  

def english_alphabet_list(request):
    english_alphabet = EnglishAlphabet.objects.all()
    return render(request, 'phonics/english_alphabet_list.html', {
        'english_alphabet': english_alphabet,
    })