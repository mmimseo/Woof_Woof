from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField

class Tag(models.Model):    # 다대다 모델
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/tag/{self.slug}/'

class Company(models.Model):    # 제조사 모델
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    ceo = models.TextField()    # 추가 필드
    tel = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/company/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Companies'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.TextField(max_length=50)
    color = models.TextField(blank=True)      # 추가 필드
    info = MarkdownxField()
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)  # 다대다 필드

    like = models.ManyToManyField(User, blank=True, related_name='like')

    def __str__(self):
        return f'[{self.pk}]{self.name} : {self.author}'

    def get_absolute_url(self):
        return f'/product/{self.pk}/'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return "https://dummyimage.com/50x50/ced4da/6c757d.jpg"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return "https://dummyimage.com/50x50/ced4da/6c757d.jpg"