from django.db import models
from core.models import Category
from gtts import gTTS  # Assuming you have gTTS installed
import os
from django.conf import settings
from django.utils.text import slugify
import string
class SoundActivity(models.Model):
    POSITION_CHOICES = [
        ('beginning', 'Beginning'),
        ('middle', 'Middle'),
        ('ending', 'Ending'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sound_activities')
    word = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sound_activities/', blank=True, null=True)
    audio = models.FileField(upload_to='sound_activities/audio/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=POSITION_CHOICES)

    def save(self, *args, **kwargs):
        if not self.audio:  # Generate audio only if it doesn't already exist
            # Generate the audio using gTTS
            tts = gTTS(self.word)
            
            # Ensure the directory exists
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'sound_activities/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Define the full path to the audio file
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            
            # Save the audio file
            tts.save(audio_path)

            # Save the relative path to the model field
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

class Blend(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blends')
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} ({self.category})"

class BlendFor(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Blend, on_delete=models.CASCADE, related_name='blend_fors')

    def __str__(self):
        return f"{self.name} ({self.type.type})"

class BlendWord(models.Model):
    blend_for = models.ForeignKey(BlendFor, on_delete=models.CASCADE, related_name='blend_words')
    word = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blend_words/', blank=True, null=True)
    audio = models.FileField(upload_to='blend_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate audio for the word using gTTS
            tts = gTTS(self.word)
            
            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'blend_words/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Define the path and save the audio file
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            tts.save(audio_path)
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word} for {self.blend_for.name}"
class Rhyming(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rhyming')
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} ({self.category})"


class RhymingFor(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Rhyming, on_delete=models.CASCADE, related_name='rhyming_fors')

    def __str__(self):
        return f"{self.name} ({self.type.type})"


class RhymingWord(models.Model):
    word = models.CharField(max_length=255)  # actual word text
    rhyming_for = models.ForeignKey(RhymingFor, on_delete=models.CASCADE, related_name='rhyming_words',null=True,blank=True)
    audio = models.FileField(upload_to='rhyming_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate audio from the word field (not from RhymingFor.name)
            tts = gTTS(self.word)
            
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'rhyming_words/audio')
            os.makedirs(audio_dir, exist_ok=True)

            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            tts.save(audio_path)

            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word} ({self.rhyming_for.name})"

class TrickyWord(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tricky_words')
    word = models.CharField(max_length=255)
    audio = models.FileField(upload_to='tricky_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate the audio file using gTTS
            tts = gTTS(self.word)
            
            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'tricky_words/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Save the file to the path
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            tts.save(audio_path)

            # Set the path to the FileField
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word} ({self.category})"

class ReadAndListen(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='read_and_listen')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    audio = models.FileField(upload_to='read_and_listen/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate the audio file using gTTS
            tts = gTTS(self.text)
            
            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'read_and_listen/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Create a filename using the heading
            audio_path = os.path.join(audio_dir, f'{self.heading}.mp3')
            tts.save(audio_path)

            # Set the path to the FileField
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.heading} ({self.category})"

class AlternativeSpelling(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='alternative_spellings')
    type = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug from the type
            self.slug = slugify(self.type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} ({self.category})"

class AlternativeSpellingWord(models.Model):
    alternative_spelling = models.ForeignKey(
        AlternativeSpelling, 
        on_delete=models.CASCADE, 
        related_name='alternative_spelling_words'
    )
    sentence = models.TextField()
    image = models.ImageField(upload_to='alternative_spelling/images/', blank=True, null=True)
    answer = models.CharField(max_length=255)
    audio = models.FileField(upload_to='alternative_spelling/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate the audio file using gTTS
            tts = gTTS(self.answer)

            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'alternative_spelling/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Save the file to the path
            audio_path = os.path.join(audio_dir, f'{self.answer}.mp3')
            tts.save(audio_path)

            # Set the path to the FileField
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.answer} ({self.alternative_spelling.type})"

class Phase(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='phases')
    phase = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.phase} ({self.category})"


# PhaseFor model linked with Phase
class PhaseFor(models.Model):
    name = models.CharField(max_length=255)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_fors')

    def __str__(self):
        return f"{self.name} ({self.phase.phase})"


# PhaseWord model linked with PhaseFor
class PhaseWord(models.Model):
    word = models.CharField(max_length=255)
    phase_for = models.ForeignKey(PhaseFor, on_delete=models.CASCADE, related_name='phase_words')
    image = models.ImageField(upload_to='phase_words/images/', blank=True, null=True)
    audio = models.FileField(upload_to='phase_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate the audio file using gTTS
            tts = gTTS(self.word)

            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'phase_words/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Save the file to the path
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            tts.save(audio_path)

            # Set the path to the FileField
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word} ({self.phase_for.name})"

class IdentifyWords(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='identify_words')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='identify_words/images/', blank=True, null=True)
    audio = models.FileField(upload_to='identify_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate the audio file using gTTS
            tts = gTTS(self.name)

            # Path setup
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'identify_words/audio')
            os.makedirs(audio_dir, exist_ok=True)

            # Save the file to the path
            audio_path = os.path.join(audio_dir, f'{self.name}.mp3')
            tts.save(audio_path)

            # Set the path to the FileField
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category})"


# IdentifyWordOption model
class IdentifyWordOption(models.Model):
    identify_word = models.ForeignKey(
        IdentifyWords,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        status = "Correct" if self.is_correct else "Wrong"
        return f"{self.option} ({status})"


class Vowel(models.Model):
    VOWEL_TYPE_CHOICES = [
        ('short', 'Short'),
        ('long', 'Long'),
    ]

    type = models.CharField(max_length=10, choices=VOWEL_TYPE_CHOICES)
    audio = models.FileField(upload_to='vowels/audio/', blank=True, null=True)
    sentence = models.TextField(blank=True)  # Auto generated sentence

    def save(self, *args, **kwargs):
        if not self.sentence:
            if self.type == 'short':
                self.sentence = f"This is a short vowel sound: {self.type}."
            else:
                self.sentence = f"This is a long vowel sound: {self.type}."

        # Generate and save the audio for the sentence
        if not self.audio:
            tts = gTTS(self.sentence)
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'vowels/audio')
            os.makedirs(audio_dir, exist_ok=True)
            audio_path = os.path.join(audio_dir, f'{self.type}_sentence.mp3')
            tts.save(audio_path)
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.get_type_display()


class VowelWord(models.Model):
    vowel = models.ForeignKey(Vowel, on_delete=models.CASCADE, related_name='vowel_words')
    word = models.CharField(max_length=255)
    image = models.ImageField(upload_to='vowel_words/images/', blank=True, null=True)
    audio = models.FileField(upload_to='vowel_words/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            tts = gTTS(self.word)
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'vowel_words/audio')
            os.makedirs(audio_dir, exist_ok=True)
            audio_path = os.path.join(audio_dir, f'{self.word}.mp3')
            tts.save(audio_path)
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.word

class VowelsAlphabet(models.Model):
    VOWEL_CHOICES = [
        ('a', 'a'),
        ('e', 'e'),
        ('i', 'i'),
        ('u', 'u'),
        ('ai', 'ai'),
        ('ee', 'ee'),
        ('ie', 'ie'),
        ('oa', 'oa'),
        ('ue', 'ue'),
    ]

    VOWEL_TYPE_CHOICES = [
        ('short', 'Short'),
        ('long', 'Long'),
    ]

    vowel = models.CharField(max_length=2, choices=VOWEL_CHOICES)
    main_type = models.CharField(max_length=10, choices=VOWEL_TYPE_CHOICES)
    word = models.CharField(max_length=255, blank=True, null=True)
    audio = models.FileField(upload_to='vowels_alphabet/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            # Generate audio for vowel sound
            tts = gTTS(self.vowel)
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'vowels_alphabet/audio')
            os.makedirs(audio_dir, exist_ok=True)
            audio_path = os.path.join(audio_dir, f'{self.vowel}.mp3')
            tts.save(audio_path)
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vowel} ({self.main_type})"

class EnglishAlphabet(models.Model):
    LETTER_CHOICES = [(letter, letter) for letter in string.ascii_uppercase]

    letter = models.CharField(max_length=1, choices=LETTER_CHOICES)
    word = models.CharField(max_length=255, blank=True, null=True)
    audio = models.FileField(upload_to='english_alphabet/audio/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.audio:
            tts = gTTS(self.letter)
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'english_alphabet/audio')
            os.makedirs(audio_dir, exist_ok=True)
            audio_path = os.path.join(audio_dir, f'{self.letter}.mp3')
            tts.save(audio_path)
            self.audio.name = os.path.relpath(audio_path, settings.MEDIA_ROOT)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.letter
