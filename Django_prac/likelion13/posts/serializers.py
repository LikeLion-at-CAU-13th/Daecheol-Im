### Model Serializer case

from rest_framework import serializers
from .models import Post, Comment
from .models import Image

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

#S3
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"