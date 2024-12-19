import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Sum
from .models import Post, Comment, Vote
from .forms import PostForm, CommentForm
from django.contrib import messages


class PostMainView(generic.ListView):
    model = Post
    template_name = 'content/posts_main.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status=1).annotate(
            comment_count=Count('comments'),
            total_votes=Sum('votes__value')
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
        messages.success(self.request, "Post submitted!")
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
            
            # Check if this is a reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                # Set the parent comment for replies
                comment.parent = get_object_or_404(Comment, id=parent_id)

            # Adding approved = True for testing
            comment.approved = True
            
            # Save the comment (either as a standalone or as a reply)
            comment.save()
            messages.success(self.request, "Comment submitted!")
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'content/add_comment.html', {'form': form})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.creator != request.user:
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'featured_image' in request.FILES:
                post.featured_image = request.FILES['featured_image']
            post.save()

            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'content/edit_post.html',
        {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        if request.user == post.creator:
            post.delete()

            messages.success(request, 'Your post has been deleted!')
            return redirect('posts_main')

    return redirect('post_detail', slug=slug)


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Comment edited!")
            return redirect('post_detail', slug=comment.post.slug)

    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'content/edit_comment.html',
        {'form': form, 'comment': comment})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(self.request, "Comment deleted!")
        return redirect('post_detail', slug=comment.post.slug)

    return render(request, 'content/delete_comment.html', {'comment': comment})


@login_required
@require_POST
def vote(request):
    try:
        data = json.loads(request.body)
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        value = data.get('value')

        if content_type == 'post':
            model = Post
        elif content_type == 'comment':
            model = Comment
        else:
            return JsonResponse(
                {'success': False,
                 'error': 'Invalid content type'},
                status=400  # Corrected status code from 40 to 400
                )

        content_type_instance = ContentType.objects.get_for_model(model)
        obj = model.objects.get(id=object_id)

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type_instance,
            object_id=object_id,
            defaults={'value': value}
        )

        if not created:
            if vote.value != int(value):
                vote.value = value
                vote.save()
            else:
                vote.delete()

        return JsonResponse({
            'success': True,
            'total_votes': obj.total_votes(),
            'user_vote': vote.value if vote.id else None
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse(
             {'success': False,
              'error': str(e)}, status=500)
