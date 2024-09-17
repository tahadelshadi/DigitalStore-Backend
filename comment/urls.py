from django.urls import path

from comment.views import CommentList

urlpatterns = [
    path("api/comment/<int:product_id>/", CommentList.as_view(), name="comment_list"),
]