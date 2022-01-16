from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [{'title': "About us", 'url_name': 'about'},
        {'title': "Add new post", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Log in", 'url_name': 'login'},
        ]


class CarsHome(ListView):
    model = Car
    template_name = "cars/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Main page"
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Car.objects.filter(is_published=True)

    # def index(request):
    #     posts = Car.objects.all()
    #     context = {
    #         'posts': posts,
    #         'cat_selected': 0,
    #         'menu': menu,
    #         'title': "Main page"
    #     }
    #     return render(request, 'cars/index.html', context=context)


def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'About us'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'cars/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Adding post"
        return context

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#         print(form)
#         return render(request, 'cars/addpage.html', {'form': form, 'menu': menu, 'title': 'Add new post'})


def contact(request):
    return HttpResponse("This is <bold>Contact</bold>")


def login(request):
    return HttpResponse("This is <bold>Log in   </bold>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1 style='color:red'>This page isn't found</h1>")


class ShowPost(DetailView):
    model = Car
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Car, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_canceled': post.cat_id,
#     }
#     return render(request, 'cars/post.html', context=context)


class CarsCategory(ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Car.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context
# def show_category(request, cat_slug):
#     cats = Category.objects.all()
#     for c in cats:
#         if c.slug == cat_slug:
#             cat_id = c.pk
#     posts = Car.objects.filter(cat_id=cat_id)
#     context = {
#         'posts': posts,
#         'cat_selected': 0,
#         'menu': menu,
#         'title': "Categories"
#     }
#     return render(request, 'cars/index.html', context=context)
