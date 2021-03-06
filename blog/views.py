from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from categories.models import Category


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

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)

        pagination_data = self.pagination_data(context.get("paginator"),
                                               context.get("page_obj"),
                                               context.get("is_paginated"))

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page_obj, is_paginated):
        if not is_paginated:
            return {}

        left = [page for page in range(page_obj.number - 4, page_obj.number)
                if page in paginator.page_range]
        remain = 4 - len(left)
        right = [page for page in range(page_obj.number + 1, page_obj.number + 5 + remain)
                 if page in paginator.page_range]
        remain = 4 - len(right)
        if remain > 0:
            left = [page for page in range(page_obj.number - 4 - remain, page_obj.number)
                    if page in paginator.page_range]
        return {"left": left,
                "right": right}


class PostDetialView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post


class ArchiveView(BlogView):
    def get_queryset(self):
        created_time__year = self.kwargs.get("year")
        created_time__month = self.kwargs.get("month")
        return super().get_queryset().filter(created_time__year=created_time__year,
                                             created_time__month=created_time__month)


def about(request):
    about_post = get_object_or_404(Post, title="About")
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    about_post.body = md.convert(about_post.body)
    return render(request, "blog/about.html", context={"about": about_post})


def get_category(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    context = {
        "category": selected_category
    }
    return render(request, "blog/category.html", context)
