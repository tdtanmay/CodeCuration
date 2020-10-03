# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCount, HitCountMixin

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    # parent = models.ForeignKey('self',blank=True, null=True,related_name='children')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'                  #categories under a parent with same
        verbose_name_plural = 'categories'    #slug

    def get_absolute_url(self):
        return reverse("list_of_post_by_category", args=[self.slug])

    def __str__(self):
        return self.name


    # def __str__(self):                           # __str__ method elaborated later in
    #     full_path = [self.name]                  # post.  use __unicode__ in place of
    #                                              # __str__ if you are using python 2
    #     k = self.parent
    #
    #     while k is not None:
    #         full_path.append(k.name)
    #         k = k.parent
    #
    #     return ' -> '.join(full_path[::-1])



class Post(models.Model, HitCountMixin):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)
    text = RichTextUploadingField()
    slug = models.SlugField(default='undefined')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    visits = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog/static/img', null=True, blank=True,
                              verbose_name="Image")
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')


    def save(self, *args, **kwargs):
        if self.slug == 'undefined' or not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'slug': self.slug})

    # def get_cat_list(self):           #for now ignore this instance method,
    #     k = self.category
    #     breadcrumb = ["dummy"]
    #     while k is not None:
    #         breadcrumb.append(k.slug)
    #         k = k.parent
    #
    #     for i in range(len(breadcrumb)-1):
    #         breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
    #     return breadcrumb[-1:0:-1]


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text


