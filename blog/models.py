from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    # slug = models.SlugField()
    # parent = models.ForeignKey("self",
    #                            blank=True,
    #                            null=True,
    #                            related_name="children")
    #
    # class Meta:
    #     unique_together = ("slug", "parent",)
    #     verbose_name_plural = "categories"
    #
    # def __str__(self):
    #     full_path = [self.name]
    #     k = self.parent
    #
    #     while k is not None:
    #         full_path.append(k.name)
    #         k = k.parent
    #
    #     return ' -> '.join(full_path[::-1])


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title: str = models.CharField(max_length=70)
    body = models.TextField()

    created_time = models.DateTimeField(blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_time"]
