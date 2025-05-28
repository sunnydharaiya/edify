from django.db import models
from django.utils.text import slugify
from gtts import gTTS
import os
from django.core.files import File
from io import BytesIO
from core.models import Category


class Reading(models.Model):
    """Main reading entry linked to a category with a name and slug."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='reading/images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Transcript(models.Model):
    """Stores transcript text and generates/stores audio from it."""
    reading = models.ForeignKey(Reading, related_name='transcripts', on_delete=models.CASCADE)
    text = models.TextField()
    slug = models.SlugField(blank=True)
    audio_file = models.FileField(upload_to='audio/transcripts/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text[:30])

        # Generate audio from text using gTTS (slow mode for kids)
        tts = gTTS(text=self.text, slow=True)
        audio_stream = BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)

        file_name = f"{self.slug}.mp3"
        self.audio_file.save(file_name, File(audio_stream), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]


class TrueFalseActivity(models.Model):
    reading = models.ForeignKey(Reading, related_name='true_false_activities', on_delete=models.CASCADE)
    statement = models.TextField()
    is_true = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.statement[:50]} - {'True' if self.is_true else 'False'}"
    
class MatchingPair(models.Model):
    reading = models.ForeignKey(Reading, related_name='matching_pairs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    response = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question} → {self.response}"