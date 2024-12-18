from django.db.models import Q
from itertools import chain
from django.shortcuts import render
from content.models import Post, Comment
from django.core.exceptions import ObjectDoesNotExist  # Add this line

def search_view(request):
    query = request.GET.get('q', '').strip()
    post_results = []
    comment_results = []

    if query:
        try:
            post_results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )[:40]

            comment_results = Comment.objects.filter(
                Q(comment_content__icontains=query)
            )[:50]

        except ObjectDoesNotExist:
            pass

    return render(
        request,
        'search/search_results.html',
        {'post_results': post_results, 'comment_results': comment_results, 'query': query}
    )
