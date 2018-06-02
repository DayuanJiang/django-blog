import os
from random import choice, sample
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "djangoblog.settings")

import django
django.setup()
from blog.models import Category, Post, Tag
from django.contrib.auth.models import User
from django.db import transaction


user = User.objects.get(username='david')


def add_post(index, created_time):
    title = "第{}章".format(index)
    post = Post.objects.get_or_create(title=title,
                                      category=choice(categories)
                                      )[0]
    post.body = ('これは第{}書の本文です。よろしくお願いいたします。'.format(index)) * 20
    post.author = user
    post.created_time = created_time
    post.modified_time = created_time
    post.save()
    return post

categories = Category.objects.all()
tags = Tag.objects.all()

now = datetime.now()


some_days = timedelta(days=1)

@transaction.atomic
def add_all_post():
    for index in range(1000):
        some_days = timedelta(days=index)
        created_time = now + some_days
        add_post(index, created_time)

Post.objects.all().delete()
add_all_post()