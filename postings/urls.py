from django.urls import path

from .views import MyPostView, CommentView

urlpatterns = [
    path("/posts", MyPostView.as_view()),
    path("/comments", CommentView.as_view()),
]