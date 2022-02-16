from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "About us", 'url_name': 'about'},
        {'title': "Add new post", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('car'))
            cache.set('cats', cats, 60)

        context['cats'] = cats
        context['menu'] = menu

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
