from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comment.forms import CommentForm
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
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        "post": post,
        "form": form,
        "comment_list": comment_list
    }


    return render(request, "blog/detail.html", context=context)


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by("-created_time")

    return render(request, 'blog/blog.html', context={'post_list': post_list,
                                                      })


def category(request, pk):
    selected_category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=selected_category,
                                    ).order_by("-created_time")
    return render(request, "blog/blog.html", context={"post_list": post_list})
