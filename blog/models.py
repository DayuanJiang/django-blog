import markdown

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils.html import strip_tags
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from uuslug import slugify

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def get_post_num(self):
    post_num = len(self.post_set.all)
    if self.children.all():
        for child in self.children.all():
            post_num += child.get_post_num()
    return post_num


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=200, blank=True)
    #    category = TreeForeignKey("Category", default="other", on_delete=models.SET_DEFAULT)
    category = models.ForeignKey("categories.Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_time"]

    def created_date_display(self):
        return self.created_time.strftime('%Y-%m-%d %H:%M')

    def modified_date_display(self):
        return self.last_modified.strftime('%Y-%m-%d %H:%M')

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:199]
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
