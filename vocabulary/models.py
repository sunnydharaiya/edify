from django.db import models
from core.models import Category  # Assuming Category is in the core app
from django.utils.text import slugify


class GenericActivity(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='activities')
    slug = models.SlugField(unique=True, blank=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MissingWord(models.Model):
    """Represents a missing word with an optional image."""
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='missing_words',null=True,blank=True)
    word = models.CharField(max_length=255)
    image = models.ImageField(upload_to='missing_words/', blank=True, null=True)

    def __str__(self):
        return self.word

class IdentifyPicture(models.Model):
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='pictures/')

    def __str__(self):
        return f"Image for {self.activity.title}"
        


class OptionAnswer(models.Model):
    picture = models.ForeignKey(
        IdentifyPicture, 
        on_delete=models.CASCADE, 
        related_name='options', 
        null=True,  # Allow null temporarily
        blank=True
    )
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} ({'Correct' if self.is_correct else 'Wrong'})"

class ImageMatchingActivity(models.Model):
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='image_matching_activities')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.activity.title}"


class ImageWordPair(models.Model):
    image_matching_activity = models.ForeignKey(ImageMatchingActivity, on_delete=models.CASCADE, related_name='image_word_pairs')
    image_1 = models.ImageField(upload_to='image_matching/')
    word_1 = models.CharField(max_length=255)
    image_2 = models.ImageField(upload_to='image_matching/')
    word_2 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.word_1} & {self.word_2}"
class SynonymAntonymActivity(models.Model):
    """
    Represents the Synonym/Antonym Activity linked to a generic activity.
    """
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='synonym_antonym_activities')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.activity.title}"


class WordPair(models.Model):
    """
    Represents a word along with two other words that are either synonyms or antonyms.
    """
    synonym_antonym_activity = models.ForeignKey(SynonymAntonymActivity, on_delete=models.CASCADE, related_name='word_pairs')
    main_word = models.CharField(max_length=255)
    synonym = models.CharField(max_length=255)
    antonym = models.CharField(max_length=255)

class PrefixSuffixActivity(models.Model):
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='prefix_suffix_activities',null=True,blank=True)
    title = models.CharField(max_length=255)
    TYPE_CHOICES = (
        ('prefix', 'Prefix'),
        ('suffix', 'Suffix'),
        ('other', 'Other'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES,default=1)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class PrefixSuffixWord(models.Model):
    prefix_suffix_activity = models.ForeignKey(PrefixSuffixActivity, on_delete=models.CASCADE, related_name='words')
    word_text = models.CharField(max_length=255)
    word = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.word_text


class PrefixSuffixOption(models.Model):
    word = models.ForeignKey(PrefixSuffixWord, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} ({'Answer' if self.is_answer else 'Option'})"

class UnscrambleActivity(models.Model):
    TYPE_CHOICES = (
        ('sentence', 'Sentence'),
        ('word', 'Word'),
    )
    activity = models.ForeignKey(GenericActivity, on_delete=models.CASCADE, related_name='unscramble_activities',null=True,blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class UnscrambleEntry(models.Model):
    activity = models.ForeignKey(UnscrambleActivity, on_delete=models.CASCADE, related_name='entries')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


