from django.db import models
from core.models import Category
from django.utils.text import slugify

class GrammarCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='grammar_categories', default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class GrammarActivity(models.Model):
    """Represents a grammar activity under a specific category."""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(GrammarCategory, on_delete=models.CASCADE, related_name='activities')

    def __str__(self):
        return self.name


class GrammarQuestion(models.Model):
    """Represents a grammar question linked to a specific activity."""
    activity = models.ForeignKey(GrammarActivity, on_delete=models.CASCADE, related_name='questions', default=1)  # Set default to an existing activity ID
    question = models.TextField()
    image = models.ImageField(upload_to='grammar/questions/', blank=True, null=True)

    def __str__(self):
        return f"{self.question[:50]}"


class GrammarOption(models.Model):
    """Represents the options for GrammarQuestion"""
    question = models.ForeignKey(GrammarQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} - {'Correct' if self.is_correct else 'Wrong'}"
 

class DragDropActivity(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(GrammarCategory, on_delete=models.CASCADE, related_name='dragdrop_activities')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
class DragDropType(models.Model):
    name = models.CharField(max_length=255)
    activity = models.ForeignKey(DragDropActivity, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name} - {self.activity.name}"


# Words linked to each dynamic field
class DragDropWord(models.Model):
    word = models.CharField(max_length=100)
    dragdrop_type = models.ForeignKey(DragDropType, on_delete=models.CASCADE, related_name='words')

    def __str__(self):
        return f"{self.word} ({self.dragdrop_type.name})"
    
class PickWordsActivity(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(GrammarCategory, on_delete=models.CASCADE, related_name='pickwords_activities')

    def __str__(self):
        return f"{self.title} - {self.category.title}"



class PickWordsSentence(models.Model):
    """Represents sentences linked to a specific PickWordsActivity."""
    activity = models.ForeignKey(PickWordsActivity, on_delete=models.CASCADE, related_name='sentences')
    sentence = models.TextField()

    def __str__(self):
        return self.sentence[:50]  # Show the first 50 characters


class PickWordsWord(models.Model):
    """Represents the words linked to a specific sentence."""
    sentence = models.ForeignKey(PickWordsSentence, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word