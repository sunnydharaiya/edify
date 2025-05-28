from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


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

class User(AbstractUser):
    categories = models.ManyToManyField(Category, blank=True, related_name='users')
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
