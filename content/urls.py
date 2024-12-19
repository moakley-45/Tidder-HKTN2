from django.urls import path
from . import views
from .views import add_comment, edit_comment, delete_comment

urlpatterns = [
    path('vote/', views.vote, name='vote'),
    path('', views.PostMainView.as_view(), name='posts_main'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/edit/', views.edit_post, name='post_edit'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path(
        'delete_comment/<int:comment_id>/',
        delete_comment,
        name='delete_comment'),
]
