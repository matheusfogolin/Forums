from django.shortcuts import redirect, render, get_object_or_404

from main.forms import PostForm
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from django.contrib.auth.decorators import login_required

def home(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    
    return render(request, "forums.html", context)

def details(request, slug):
    post = get_object_or_404(Post, slug=slug)   
    
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)
    
    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        comment_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=comment_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply)
    
    context = {
        "post": post
    }
    update_views(request, post)
    
    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved = True, categories = category)
    
    context = {
        "posts": posts,
        "category": category,
    }
    
    return render(request, "posts.html", context)

@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    
    context.update({
        "form": form,
        "title": "Create New Post"
    })
    
    return render(request, "create_post.html", context)