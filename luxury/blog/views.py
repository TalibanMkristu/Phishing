from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin #restrict class based views

# Create your views here.

# @login_required(login_url = "login")
def posts(request):
    blogs = Post.objects.all()
    context = {
        "blogs": blogs,

    }

    return render(request, "blog/posts.html", context )

def msrTest(request):
    return render(request, 'blog/msrTest.html')

def individual_posts(request, pk):
    blog = Post.objects.get(id=pk)
    context = {
        'blog': blog
    }
    return render(request, "blog/individualPosts.html", context)
