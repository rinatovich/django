from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import DataMixin

menu = [{'title': "About us", 'url_name': 'about'},
        {'title': "Add new post", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Log in", 'url_name': 'login'},
        ]


class CarsHome(DataMixin, ListView):
    model = Car
    template_name = "cars/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Car.objects.filter(is_published=True).select_related('cat')

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


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add page')

        return dict(list(context.items()) + list(c_def.items()))


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


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'cars/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("This is <bold>Log in   </bold>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1 style='color:red'>This page isn't found</h1>")


class ShowPost(DataMixin, DetailView):
    model = Car
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


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


class CarsCategory(DataMixin, ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Car.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


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

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))


def LogoutUser(request):
    logout(request)
    return redirect('login')
