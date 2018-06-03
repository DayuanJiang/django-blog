from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comment.forms import CommentForm
import markdown

from django.views.generic import ListView


# Create your views here.
def index(request):
    return render(request, "blog/index.html")


def blog(request):
    post_list = Post.objects.all()
    return render(request, 'blog/blog.html', context={'post_list': post_list})


class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'


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
class ArchiveView(BlogView):
    def get_queryset(self):
        created_time__year = self.kwargs.get("year")
        created_time__month = self.kwargs.get("month")
        return super().get_queryset().filter(created_time__year=created_time__year,
                                             created_time__month = created_time__month)


def category(request, pk):
    selected_category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=selected_category,
                                    ).order_by("-created_time")
    return render(request, "blog/blog.html", context={"post_list": post_list})


class CategoryView(BlogView):

    def get_queryset(self):
        selected_category = get_object_or_404(Category,
                                              pk=self.kwargs.get("pk")
                                              )

        return super().get_queryset().filter(category=selected_category)