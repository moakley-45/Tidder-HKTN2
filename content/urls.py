from django.urls import path
from . import views
from .views import add_comment, edit_comment, delete_comment


urlpatterns = [
    path('', views.PostMainView.as_view(), name='posts_main'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]
