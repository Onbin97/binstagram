from django.urls import path

from .views import MyPostView

urlpatterns = [
    path("/posts", MyPostView.as_view()),
]