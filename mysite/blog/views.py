from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm

from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)

# Create your views here.
# Class Based Views
class AboutView(TemplateView):
    '''This view represents "About" page'''
    template_name = 'about.html'

class PostListView(ListView):
    '''This view represents a page with a list of blog posts'''
    model = Post

    def get_queryset(self):
        '''This method is to query the list of blog posts based on published date'''
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    '''This view represents the details page of a blog post'''
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    '''This view represents creation of a blog post'''
    #To create a blog post, user must be logged in, hence a login_required
    #decorator is needed. LoginRequiredMixin provides that for this CreateView
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    '''This view represents updating a blog post'''
    #To update a blog post, user must be logged in, hence a login_required
    #decorator is needed. LoginRequiredMixin provides that for this UpdateView
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    '''This view represents deletion of a blog post'''
    #To delete a blog post, user must be logged in, hence a login_required
    #decorator is needed. LoginRequiredMixin provides that for this DeleteView
    model = Post
    success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin,ListView):
    '''This view represents draft posts that arent published yet'''
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#====================================================================
#Function Based Views

@login_required
def post_publish(request,pk):
    '''This function based view publishes a blog post and
        redirects to post detail page after publishing'''
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)


#@login_required
def add_comment_to_post(request,pk):
    '''This view adds comments to a blog post and redirects to post detail
        page'''
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    '''This view approves comments and redirects to post detail page'''
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    '''This view removes/deletes comments and redirects to post detail page'''
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)
