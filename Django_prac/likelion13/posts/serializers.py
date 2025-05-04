### Model Serializer case

from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

  class Meta:
		# � ���� �ø���������� ����
    model = Post
		# �𵨿��� � �ʵ带 ��������
		# ���� �������� ���� ��
    fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

  class Meta:
		# � ���� �ø���������� ����
    model = Comment
		# �𵨿��� � �ʵ带 ��������
		# ���� �������� ���� ��
    fields = "__all__"