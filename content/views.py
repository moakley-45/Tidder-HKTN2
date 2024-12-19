from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import TemplateView

class PostMainView(generic.ListView):
    model = Post
    template_name = 'content/posts_main.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status=1).annotate(
            comment_count=Count('comments')
        ).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Posts'
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    success_url = reverse_lazy('posts_main')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "content/post_detail.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        context['comment_form'] = CommentForm()
        return context

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            # adding approved = True for testing
            comment.approved = True
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'content/add_comment.html', {'form': form})

# Post edit view

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ensure only the creator can edit
    if post.creator != request.user:
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'content/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        if request.user == post.creator:
            post.delete()
            return redirect('posts_main')
        else:
            return redirect('posts_main', slug=slug)
    else:
        return redirect('post_detail', slug=slug)
