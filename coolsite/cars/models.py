from django.db import models

# Create your models here.
from django.urls import reverse


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name='загаловок')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Картинка')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    time_upload = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
        ordering = ['id']