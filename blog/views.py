from django.shortcuts import render, get_object_or_404
from .models import Post

import markdown


# Create your views here.
def index(request):
    return render(request, "blog/index.html")


def blog(request):
    post_list = Post.objects.all().order_by('-created_time')[:10]
    return render(request, 'blog/blog.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request, "blog/detail.html", context={"post": post})
