from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'featured_image', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Check if it's an existing post (editing), not a new post (creating)
        if self.instance.pk:  # If the post has a primary key, it's being edited
            self.helper.add_input(Submit('submit', 'Save Changes'))  # Change button text for editing
        else:
            self.helper.add_input(Submit('submit', 'Create Post'))  # Use original button for creating posts
        self.helper.layout = Layout(
            Field('title'),
            Field('content', rows=4),
            Field('excerpt', rows=2),
            Field('featured_image'),
            Field('status'),
        )

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
