from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

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
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'content/add_comment.html', {'form': form})
