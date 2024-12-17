from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostMainView.as_view(), name='posts_main'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
