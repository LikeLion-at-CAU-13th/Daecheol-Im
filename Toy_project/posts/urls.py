from django.urls import path
from posts.views import *

urlpatterns = [
    path('', post_list), # �Խñ� ���� �� ��ȸ
    path('<int:post_id>/', post_delete), #�Խñ� ����
]