from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"), (2, "Hidden"))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    featured_image = CloudinaryField(
        'image',
        default='placeholder')
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # votes = GenericRelation(Vote)

    # def total_votes(self):
    #     return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0
    
    

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    # parent = models.ForeignKey(
    # 'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_content = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    # votes = GenericRelation(Vote)

    # def total_votes(self):
    #     return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0
    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


# class Vote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASADE)
#     object_id = models.PostitiveField()
#     content_object = GenericForeignKey ('content_type', 'object_id')
#     value = models.SmallIntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))
#     created_at = models.DateTImeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'content_type', 'object_id')