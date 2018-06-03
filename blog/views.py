from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comment.forms import CommentForm
import markdown

from django.views.generic import ListView, DetailView


# Create your views here.
def index(request):
    return render(request, "blog/index.html")

class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'
    paginate_by = 10

class PostDetialView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        update_data = {
            "form": form,
            "comment_list": comment_list
        }
        context.update(update_data)
        return context

class ArchiveView(BlogView):
    def get_queryset(self):
        created_time__year = self.kwargs.get("year")
        created_time__month = self.kwargs.get("month")
        return super().get_queryset().filter(created_time__year=created_time__year,
                                             created_time__month=created_time__month)


class CategoryView(BlogView):

    def get_queryset(self):
        selected_category = get_object_or_404(Category,
                                              pk=self.kwargs.get("pk")
                                              )
        return super().get_queryset().filter(category=selected_category)
