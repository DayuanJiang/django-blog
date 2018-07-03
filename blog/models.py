from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# # Create your models here.
# class Category(MPTTModel):
#     name = models.CharField(max_length=200)
#     parent = TreeForeignKey("self",
#                             null=True, blank=True,
#                             related_name="children",
#                             db_index=True,
#                             on_delete=models.CASCADE)
#     slug = models.SlugField()
#
#     class MPTTMeta:
#         order_insertion_by = ["name"]
#
#     class Meta:
#         unique_together = (("parent", "slug",))
#         verbose_name_plural = "categories"
#
#     def get_slug_list(self):
#         try:
#             ancestors = self.get_ancestors(include_self=True)
#         except:
#             ancestors = []
#         else:
#             ancestors = [i.slug for i in ancestors]
#         slugs = []
#         for i in range(len(ancestors)):
#             slugs.append('/'.join(ancestors[:i + 1]))
#         return slugs
#
#     def __str__(self):
#         return self.name
#
#     # slug = models.SlugField()
#     # parent = models.ForeignKey("self",
#     #                            blank=True,
#     #                            null=True,
#     #                            related_name="children")
#     #
#     # class Meta:
#     #     unique_together = ("slug", "parent",)
#     #     verbose_name_plural = "categories"
#     #
#     # def __str__(self):
#     #     full_path = [self.name]
#     #     k = self.parent
#     #
#     #     while k is not None:
#     #         full_path.append(k.name)
#     #         k = k.parent
#     #
#     #     return ' -> '.join(full_path[::-1])


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now=True)
    #modified_time = models.DateTimeField(blank=True, null=True)
    excerpt = models.CharField(max_length=200, blank=True)
#    category = TreeForeignKey("Category", default="other", on_delete=models.SET_DEFAULT)
    category = models.ForeignKey("categories.Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
# https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_time"]
