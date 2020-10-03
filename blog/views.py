# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hitcount.views import HitCountDetailView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

from blog.models import Post,Comment,Category
from blog.forms import PostForm, CommentForm, ContactForm


from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import F
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse # Add this

from .forms import ContactForm # Add this


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.order_by('name')
        return context


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True

    # def get_object(self):
    #     post = get_object_or_404(Post, slug=self.kwargs['slug'])
    #     post.visits += 1
    #     post.save()
    #
    #     self.view_count = post.visits
    #     return post
    #
    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['view_count'] = self.view_count
    #     return context



class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('Post_List')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#######################################################################################################################


@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)

def list_post_by_category(request, category_slug):
    categories = Category.objects.all()
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post = post.filter(category=category)
        template = 'blog/list_of_post_by_category.html'
        context = {'categories': categories, 'post': post, 'category': category}
        return render(request, template, context)


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})



@login_required
def comment_approve(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    comment.approve()
    return redirect('post_detail', slug=comment.post.slug)

@login_required
def comment_remove(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    post_slug = comment.post.slug
    comment.delete()
    return redirect('post_detail', slug=post_slug)

from django.core.mail import send_mail

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']

            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            send_mail('New Enquiry', message, sender_email, ['tdtanmay8@gmail.com'])
            return HttpResponse('Thanks for contacting us!')
    else:
        form = ContactForm()

    return render(request, 'blog/contact-us.html', {'form': form})
