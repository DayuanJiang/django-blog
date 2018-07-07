from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r"blog/", views.BlogView.as_view(), name="blog"),
    path(r"blog/<int:pk>/", views.PostDetialView.as_view(), name="detail"),
    path(r"archive/<int:year>/<int:month>/", views.ArchiveView.as_view(), name="archive"),
    path("category/<int:pk>/",views.get_category,name="category")
]
