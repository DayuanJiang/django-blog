import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "djangoblog.settings")

import django

django.setup()
from blog.models import Category, Post, Tag
from django.db import transaction


def add_tag(name):
    if name:
        tag = Tag.objects.get_or_create(name=name)[0]
        tag.save()
        return tag


def add_category(name):
    if name:
        category = Category.objects.get_or_create(name=name)[0]
        category.save()
        return category


category_list = """ 
Art Punk
Alternative Rock
College Rock
Crossover Thrash 
Crust Punk 
Experimental Rock
Folk Punk
Goth 
Grunge
Hardcore Punk
Hard Rock
Indie Rock
Lo-fi
New Wave
Progressive Rock
Punk
""".split("\n")

tag_list = """
pop chill indie love rock happy electronic indie rock
alternative hip hop sad summer dance party study Ed 
Sheeran relax rap acoustic folk sleep punk
""".split()


@transaction.atomic
def add_all_categorys():
    for category in category_list:
        add_category(category)


@transaction.atomic
def add_all_tags():
    for tag in tag_list:
        add_tag(tag)


Category.objects.all().delete()
Tag.objects.all().delete()
add_all_categorys()
add_all_tags()
