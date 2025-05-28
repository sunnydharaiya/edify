from django import template
import random

register = template.Library()

@register.filter
def shuffle(value):
    """Shuffles a list in place."""
    temp_list = list(value)  # Make a copy
    random.shuffle(temp_list)
    return temp_list

@register.filter
def get(obj, key):
    """Returns the value for a given key from a dictionary."""
    return obj.get(key, [])

@register.filter
def filter(queryset, field):
    """Groups queryset items by a specified field into a dictionary."""
    result = {}
    for item in queryset:
        key = getattr(item, field)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result
@register.filter
def random_indices(length, count=2):
    try:
        length = int(length)
    except (TypeError, ValueError):
        return []
    if length <= count:
        return list(range(length))
    return random.sample(range(length), count)

@register.simple_tag
def replace_indices(word, indices, replacement='_'):
    word_list = list(word)
    for index in indices:
        if 0 <= index < len(word_list):
            word_list[index] = replacement
    return ''.join(word_list)

@register.simple_tag
def letters_at_indices(word, indices):
    return [word[i] for i in indices if 0 <= i < len(word)]

@register.filter
def make_range(value):
    try:
        return range(int(value))
    except Exception:
        return range(0)

@register.filter
def split(value, delimiter):
    return value.split(delimiter)

@register.filter
def filter_word(queryset, word):
    return queryset.filter(word__iexact=word).exists()