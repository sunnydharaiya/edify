from django.shortcuts import render, get_object_or_404
from .models import Blog

def index_view(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'index.html', context)

def about_view(request):
    context = {
        'title': 'About',
    }
    return render(request, 'about.html', context)

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})
