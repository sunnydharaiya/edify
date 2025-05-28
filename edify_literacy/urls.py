"""
URL configuration for edify_literacy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import index_view,about_view,blog_list,blog_detail
from reading.views import reading_detail
from activity.views import spelling_drag_drop, long_vowel_sound, unscramble_activity, expression_group_detail, vowel_word
from phonics.views import vowel_word_list, sound_activity_list, blend_list, blend_for_list,english_alphabet_list
from phonics.views import rhyming_list,tricky_word_list,phase_view,read_listen_list,alternative_spelling_list,alternative_spelling_detail,identify_words_list
from vocabulary.views import generic_activity_detail
from grammar.views import gramamr_activity_list,grammar_activity_detail,dragdrop_activity_detail,pick_words_activity_detail
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('about', about_view, name='about'),
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<int:pk>/', blog_detail, name='blog_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login_modal.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('reading/<slug:slug>/', reading_detail, name='reading_detail'),
    path('spelling-drag-drop/', spelling_drag_drop, name='spelling_drag_drop'),
    path('long-vowel-sound/', long_vowel_sound, name='long_vowel_sound'),
    path('unscramble-activity/', unscramble_activity, name='unscramble_activity'),
    path('expression-group/<slug:slug>/', expression_group_detail, name='expression_group_detail'),
    path('vowel-word/', vowel_word, name='vowel_word'),

    path('vowel-words/<str:type>/', vowel_word_list, name='vowel_word_list'),
    path('sound-activities/<str:position>/<str:level>/', sound_activity_list, name='sound_activity_list'),
    path('blends/<str:level>/', blend_list, name='blend_list'),
    path('blends/detail/<int:blend_id>/', blend_for_list, name='blend_for_list'),
    path('rhyming-words/<str:level>/', rhyming_list, name='rhyming_list'),
    path('tricky-words/<str:level>/', tricky_word_list, name='tricky_word_list'),
    path('phase/<str:phase>/', phase_view, name='phase_view'),
    path('read-listen/<str:level>/', read_listen_list, name='read_listen_list'),
    path('alternative-spelling/<str:level>/', alternative_spelling_list, name='alternative_spelling_list'),
    path('alternative-spelling/detail/<slug:slug>/', alternative_spelling_detail, name='alternative_spelling_detail'),
    path('identify-words/<str:level>/', identify_words_list, name='identify_words_list'),
    path('english-alphabet/', english_alphabet_list, name='english_alphabet_list'),


    path('category/<str:category_slug>/<str:activity_slug>/', generic_activity_detail, name='generic_activity_detail'),
    path('grammar/<str:category_slug>/<str:activity_slug>/', gramamr_activity_list, name='gramamr_activity_list'),
    path('grammar/activity/<str:category_slug>/<str:activity_name>/', grammar_activity_detail, name='grammar_activity_detail'),
    path('dragdrop/<str:activity_slug>/', dragdrop_activity_detail, name='dragdrop_activity_detail'),
    path('pick-activity/<str:category_slug>/<str:activity_slug>/', pick_words_activity_detail, name='pick_words_activity_detail'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)