from django.urls import path
from post.views import *

urlpatterns = [
    path("", index, name="index"),
    path("create-post", create_post, name="create_post"),
    path("<uuid:post_id>", PostDetail, name="post_detail"),
    path("like<uuid:post_id>", LikePost, name="like_post"),
    path("search/", search_view, name="search"),

]
