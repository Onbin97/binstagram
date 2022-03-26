from django.urls import path

from .views import MyPostView, CommentView, LikeView

urlpatterns = [
    path("/posts", MyPostView.as_view()),
    path("/comments", CommentView.as_view()),
    path("/likes", LikeView.as_view()),
]