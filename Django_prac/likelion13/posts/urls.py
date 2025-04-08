from django.urls import path
from posts.views import *

urlpatterns = [

		#path("", hello_world, name="hello_world"),
    #path("page", index, name="my-page"),
    #path('<int:id>', get_post_detail),

    path('', post_list, name="post_list"),
    path('<int:post_id>/', post_detail, name='post_detail'), 
    path('posts/<int:post_id>/comments/', get_comment_all, name='comment_list_by_post'), # 게시글에 달린 댓글 조회
    path('categories/<int:category_id>/posts/', posts_by_category, name='posts_by_category'), # 카테고리에 해당하는 게시글 조회
]