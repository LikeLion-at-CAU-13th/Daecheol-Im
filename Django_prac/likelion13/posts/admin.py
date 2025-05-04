from django.contrib import admin
from .models import Post, Comment, Category, PostCategory

# Register your models here.
# PostCategory�� Inline���� ����
class PostCategoryInline(admin.TabularInline):  # �Ǵ� StackedInline
    model = PostCategory
    extra = 1  # ���� �߰� ������ ���� ��

# Post Admin�� Inline �߰�
class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)