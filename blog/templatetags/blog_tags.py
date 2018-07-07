from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


@register.simple_tag
def archives(num=5):
    dates = Post.objects.dates('created_time', 'month', order='DESC')[:num]
    return_data = []
    for date in dates:
        count = Post.objects.filter(created_time__year=date.year,
                                    created_time__month=date.month).count()
        return_data.append((date.year, date.month, count))

    return return_data


@register.simple_tag
def get_view_rank(num=5):
    return Post.objects.order_by("-hit_count_generic__hits")[:num]
