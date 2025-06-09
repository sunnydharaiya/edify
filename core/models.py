from django.db import models


class ClassificationType(models.TextChoices):
    GRADE = 'grade', 'Grade Wise'
    LEVEL = 'level', 'Level Wise'
    NONE = 'none', 'None/Direct'

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    classification_type = models.CharField(max_length=10, choices=ClassificationType.choices)
    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/images/')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
