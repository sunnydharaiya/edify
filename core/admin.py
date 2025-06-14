from django.contrib import admin
from .models import Category,Blog
from ckeditor.widgets import CKEditorWidget
from django import forms



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification_type',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')








