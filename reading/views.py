from gtts import gTTS
import os
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from .models import Reading,MatchingPair

def generate_audio(text, filename):
    tts = gTTS(text)
    filepath = f'media/audio/transcripts/{filename}.mp3'
    tts.save(filepath)
    return filepath

def reading_detail(request, slug):
    reading = get_object_or_404(Reading, slug=slug)
    
    # Fetching related objects
    transcripts = reading.transcripts.all()
    true_false_activities = reading.true_false_activities.all()
    matching_pairs = MatchingPair.objects.filter(reading=reading)

    # Convert to list of dictionaries
    matching_pairs_data = list(matching_pairs.values('question', 'response'))
    
    context = {
        'reading': reading,
        'transcripts': transcripts,
        'true_false_activities': true_false_activities,
        'matching_pairs': matching_pairs_data
    }
    return render(request, 'reading/reading_detail.html', context)

