from django.contrib import admin
from .models import Post, Comment, Category, PostCategory

# Register your models here.
# PostCategory를 Inline으로 정의
class PostCategoryInline(admin.TabularInline):  # 또는 StackedInline
    model = PostCategory
    extra = 1  # 새로 추가 가능한 라인 수

# Post Admin에 Inline 추가
class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)