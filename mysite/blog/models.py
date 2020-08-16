from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    '''Model to represent a blog post'''
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        #This method will publish the blog post
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        #This method will approve comments on the blog post
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        #This method will redirect to post detail page after submitting a blog post
        return reverse('blog:post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        #String representation of the blog post
        return self.title

class Comment(models.Model):
    '''Model to represent comments on the blog post'''
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        #This method represents approval of a comment on a blog post
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        #This method will redirect to list of posts page after submitting a comment
        return reverse('blog:post_list')

    def __str__(self):
        #String representation of the comment
        return self.text
