from django.db import models
from accounts.models import User

# Create your models here.
# 추상 클래스 정의
class BaseModel(models.Model): # models.Model을 상속받음
    created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True

class Category(models.Model): # 카테고리 기능
    name = models.CharField(max_length=30)
    cat_id = models.AutoField(primary_key=True) # cat pk 추가

    def __str__(self):
        return self.name

class Post(BaseModel): # BaseModel을 상속받음

    CHOICES = (
        ('STORED', '보관'),
        ('PUBLISHED', '발행')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=CHOICES, default='STORED')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return self.title

class PostCategory(models.Model):
    PC_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')

    
class Comment(BaseModel):
    com_id = models.AutoField(primary_key=True) # comment pk 추가
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=50) # 댓글 단 사람 : 댓글 작성시 입력
    content = models.TextField() # 댓글 내용 입력

    def __str__(self):
        return f'{self.author_name} - {self.content[:20]}' # 작성자 이름과 댓글 내용 일부 보여줌