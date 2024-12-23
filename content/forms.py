from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Post, Comment
from django.utils.text import slugify


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'featured_image', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Check if it's an existing post (editing), not a new post (creating)
        if self.instance.pk:
            self.helper.add_input(Submit('submit', 'Save Changes'))
        else:
            self.helper.add_input(Submit('submit', 'Create Post'))
        self.helper.layout = Layout(
            Field('title'),
            Field('content', rows=4),
            Field('excerpt', rows=2),
            Field('featured_image'),
            Field('status'),
        )

    def save(self, commit=True):
        post = super().save(commit=False)
        post.slug = slugify(post.title)
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Comment'))
        self.helper.layout = Layout(
            Field('comment_content', rows=3),
        )
