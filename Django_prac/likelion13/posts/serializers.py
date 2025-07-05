### Model Serializer case
from rest_framework import serializers
from .models import Post, Comment, User
from .models import Image

#14주차
from config.custom_api_exceptions import PostConflictException

class PostSerializer(serializers.ModelSerializer):
  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Post
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때
    fields = "__all__"
  
  # 14주차 중복된 게시글 제목이 있다면 예외 발생
  def validate(self, data):
    from datetime import datetime, time
    from django.utils import timezone

    user = data.get('user')

    # user가 ID(int)일 경우 User 객체로 변환
    if isinstance(user, int):
        user = User.objects.get(pk=user)
    elif not isinstance(user, User):
        raise serializers.ValidationError("유효하지 않은 사용자입니다.")

    now = timezone.now()
    start = timezone.make_aware(datetime.combine(now.date(), time.min))
    end = timezone.make_aware(datetime.combine(now.date(), time.max))

    # 중복 제목 검사
    if Post.objects.filter(title=data['title']).exists():
        raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")

    # 하루 1개 제한
    post_count_today = Post.objects.filter(user=user, created__range=(start, end)).count()
    if post_count_today >= 1:
        raise serializers.ValidationError("하루에 하나만 게시글을 작성할 수 있습니다.")

    data['user'] = user  # 객체로 설정

    return data

class CommentSerializer(serializers.ModelSerializer):

  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Comment
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때
    fields = "__all__"

  def validate_content(self, value):
        if len(value.strip()) < 15:
            raise serializers.ValidationError("댓글은 최소 15자 이상 작성해주세요.")
        return value

#S3
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"