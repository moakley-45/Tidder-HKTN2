from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages

# Create your views here.

class PostMainView(generic.ListView):
    model = Post
    template_name = "content/posts_main.html"
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        return Posts.objects.all().order_by('-created_on')