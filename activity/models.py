from django.db import models
from core.models import Category
from django.utils.text import slugify
import random
from gtts import gTTS
import os
from django.conf import settings

class SpellingGroup(models.Model):
    """Represents a group of Spelling Types (e.g., Long E sound, Short I sound)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spelling_groups')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Ensure the default exists before the migration
def get_default_group():
    group, _ = SpellingGroup.objects.get_or_create(name='Default Group', category_id=1, slug='default-group')
    return group.id


class SpellingType(models.Model):
    group = models.ForeignKey(SpellingGroup, on_delete=models.CASCADE, related_name='spelling_types', default=get_default_group)
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.group.name})"

class SpellingWord(models.Model):
    """Represents individual words that belong to a SpellingType"""
    spelling_type = models.ForeignKey(SpellingType, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/spelling_words/', blank=True, null=True)

    def __str__(self):
        return f"{self.word} → {self.spelling_type.name}"
    
class LongVowelSound(models.Model):
    """Represents a Long Vowel Sound with associated image, audio, and category"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='long_vowel_sounds')
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/long_vowel_sounds/')
    audio = models.FileField(upload_to='audio/long_vowel_sounds/', blank=True, null=True)
    is_correct = models.BooleanField(default=True)  # Yes/No option

    def __str__(self):
        return f"{self.word} - {'Correct' if self.is_correct else 'Incorrect'}"
    
class UnscrambleActivity(models.Model):
    """Model for Unscramble Word Activity with linked sentences"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='unscramble_activities')
    sentence_part_1 = models.TextField(help_text="Sentence part before the blank space")
    sentence_part_2 = models.TextField(help_text="Sentence part after the blank space")
    word = models.CharField(max_length=100)  # Correct word for the blank
    scrambled_word = models.CharField(max_length=100, blank=True)  # Scrambled version of the word
    image = models.ImageField(upload_to='images/unscramble_activities/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.scrambled_word:
            self.scrambled_word = self._scramble_word(self.word)
        super().save(*args, **kwargs)

    def _scramble_word(self, word):
        """Utility function to scramble the word"""
        word_list = list(word)
        random.shuffle(word_list)
        return ''.join(word_list)

    def __str__(self):
        return f"{self.sentence_part_1} ____ {self.sentence_part_2} - [{self.scrambled_word}]"
    
class ExpressionGroup(models.Model):
    """Represents different groups of expressions (e.g., Emotions, Actions, Objects, etc.)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expression_groups')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ExpressionObject(models.Model):
    """Represents the main expression object with image and linked options"""
    group = models.ForeignKey(ExpressionGroup, on_delete=models.CASCADE, related_name='expression_objects')
    image = models.ImageField(upload_to='images/expression_objects/', blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} Object"


class ExpressionOption(models.Model):
    """Represents multiple options linked to an ExpressionObject"""
    expression_object = models.ForeignKey(ExpressionObject, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)  # You can have multiple correct ones

    def __str__(self):
        status = "✔" if self.is_correct else "✘"
        return f"{self.option_text} {status}"

class VowelWord(models.Model):
    """Represents a word with a vowel type (short/long) and auto-generated audio."""
    SHORT = 'short'
    LONG = 'long'

    VOWEL_TYPE_CHOICES = [
        (SHORT, 'Short'),
        (LONG, 'Long'),
    ]
    
    word = models.CharField(max_length=100)
    vowel_type = models.CharField(
        max_length=5,
        choices=VOWEL_TYPE_CHOICES,
        default=SHORT
    )
    audio_file = models.FileField(upload_to='audio/vowel_words/', blank=True, null=True)  # Audio file

    def save(self, *args, **kwargs):
        if not self.audio_file:  # Generate audio only if no audio file exists
            # Generate the audio using gTTS
            tts = gTTS(self.word)
            
            # Ensure the directory exists
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio', 'vowel_words')
            os.makedirs(audio_dir, exist_ok=True)  # Create the directory if it doesn't exist
            
            # Define the full path to the audio file
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            
            # Save the audio file
            tts.save(audio_path)
            self.audio_file = os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path to the audio file
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word} ({self.get_vowel_type_display()})"