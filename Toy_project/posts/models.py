from django.db import models
#from accounts.models import User

# Create your models here.
# 추상 클래스 정의
class BaseModel(models.Model): # models.Model을 상속받음
    created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True


class Post(BaseModel): # BaseModel을 상속받음
    id = models.AutoField(primary_key=True) # 게시글 id
    title = models.CharField(max_length=30) # 제목
    content = models.TextField() # 작성 내용
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    password = models.CharField(max_length=20) # 비밀번호 최대 20자리
    name = models.CharField(max_length=50, default="익명") # 작성자 이름

    def __str__(self):
        return self.title