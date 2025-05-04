from django.urls import path
from posts.views import *

urlpatterns = [
    path('', post_list), # 게시글 생성 및 조회
    path('<int:post_id>/', post_delete), #게시글 삭제
]