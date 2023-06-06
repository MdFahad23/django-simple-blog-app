from django.urls import path


from . import views

app_name = "App_Blog"

urlpatterns = [
    path("", views.Blog_List.as_view(), name="blog_list"),
    path("write/", views.CreateBlog.as_view(), name="create_blog"),
    path(
        "details/(?P<slug>[-a-zA-Z0-9_\-]+)/",
        views.blog_details,
        name="blog_details",
    ),
    path("liked/<pk>/", views.liked, name="liked_post"),
    path("un-liked/<pk>/", views.unLiked, name="unLiked_post"),
    path("my-blog/", views.MyBlogs.as_view(), name="my-blog"),
    path("edit/<pk>", views.EditBlog.as_view(), name="edit-blog"),
]
