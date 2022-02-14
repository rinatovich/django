from django.db.models import Count

from .models import *

menu = [{'title': "About us", 'url_name': 'about'},
        {'title': "Add new post", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Log in", 'url_name': 'login'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['cats'] = cats
        context['menu'] = menu

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
