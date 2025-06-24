from django.urls import path
from posts.views import *

urlpatterns = [
    
    #함수 기반 뷰(FBV)
    #ath('', post_list, name="post_list"),
    #path('<int:post_id>/', post_detail, name='post_detail'), 
    #path('posts/<int:post_id>/comments/', get_comment_all, name='comment_list_by_post'), # 게시글에 달린 댓글 조회
    #path('categories/<int:category_id>/posts/', posts_by_category, name='posts_by_category'), # 카테고리에 해당하는 게시글 조회
    
    
    #클래스 기반 뷰(CBV)
    path('', PostList.as_view()), # post 전체 조회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회
    path('<int:post_id>/comments/', CommentList.as_view()), # 해당 게시글의 모든 댓글 조회
    
    #S3
    path('upload/', ImageUploadView.as_view(), name='image-upload')
]