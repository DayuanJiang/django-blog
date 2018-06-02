from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r"blog/",views.blog, name="blog"),
    path(r"blog/<int:pk>/", views.detail, name="detail"),
]