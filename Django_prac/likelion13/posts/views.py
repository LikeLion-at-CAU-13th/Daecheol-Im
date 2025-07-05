import json
import uuid

#함수형 뷰(FBV)
from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_http_methods
from .models import *
#클래스형 뷰(CBV)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import PostSerializer, CommentSerializer

#인가
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import TimeAndOwnerPermission

from django.core.files.storage import default_storage  
from .serializers import ImageSerializer
from django.conf import settings
import boto3

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.parsers import MultiPartParser, FormParser

#14주차 예외처리
from config.custom_exceptions import PostNotFoundException

# 함수형 뷰(FBV)로 구현
# 게시글에 달린 댓글 모두 불러오기
'''@require_http_methods(["GET"])
def get_comment_all(reqeust, post_id): # 인자로 게시글의 id를 받음
    post = get_object_or_404(Post, pk=post_id) # Post 클래스에서 pk가 입력받은 인자와 같은 객체를 post에 담음
    comments = Comment.objects.filter(post=post) # Comment의 객체중 post_id가 입력받은 인자와 같은 객체들을 comments에 담음

    comment_json_list = [] # 댓글들 저장하는 리스트
    for comment in comments:
        comment_json_list.append({
            "id": comment.com_id,
            "author_name": comment.author_name,
            "content": comment.content,
            "created": comment.created,
        })

    return JsonResponse({
        "status": 200,
        "message": f"게시글 {post_id}번에 달린 댓글 목록",
        "data": comment_json_list
    })

def posts_by_category(request, category_id):# 인자로 카테고리의 id를 받음
    category = get_object_or_404(Category, pk=category_id) # Category 클래스에서 pk가 입력받은 인자와 같은 객체를 category에 담음

    post_categories = PostCategory.objects.filter(category=category).order_by('-post__created') # 이 카테고리에 속한 PostCategory들을 최신순 정렬

    post_json_list = []
    for pc in post_categories:
        post = pc.post # 해당 PostCategory에 대응하는 Post를 post에 담음
        post_json_list.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "created": post.created,
            "user": post.user.username,
            "categories": [cat.category.name for cat in post.post_categories.all()]
        })

    return JsonResponse({
        'status': 200,
        'message': f'"{category.name}" 카테고리의 게시글 목록입니다.',
        'data': post_json_list
    })

    #게시글 일부 조회
def get_post_detail(reqeust, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "status" : post.status,
        "user" : post.user.username,
        "categories": [category.name for category in post.post_categories.all()]
    }
    return JsonResponse({
        "status" : 200,
        "data": post_detail_json})

# 게시글 생성 및 게시글 모두 조회
@require_http_methods(["POST", "GET"])
def post_list(request):
    
    if request.method == "POST":
    
        body = json.loads(request.body.decode('utf-8'))
    
        user_id = body.get('user')
        user = get_object_or_404(User, pk=user_id)

        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            status = body['status'],
            user = user
        )

        category_ids = body.get('categories', [])  # 카테고리 ID 리스트
        for cat_id in category_ids:
            category = get_object_or_404(Category, pk=cat_id)
            PostCategory.objects.create(post=new_post, category=category)

        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content": new_post.content,
            "status": new_post.status,
            "user": new_post.user.id,
            "categories": category_ids
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json

        })

        # 게시글 전체 조회
    if request.method == "GET":
        post_all = Post.objects.all()
    
		# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id,
                "categories": [category.name for category in post.post_categories.all()]
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all

        })

@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        post = get_object_or_404(Post, pk=post_id)

        post_json = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id,
        }
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 단일 조회 성공',
            'data': post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=post_id)

        if 'title' in body:
            update_post.title = body['title']
        if 'content' in body:
            update_post.content = body['content']
        if 'status' in body:
            update_post.status = body['status']
    
        
        update_post.save()

        update_post_json = {
            "id": update_post.id,
            "title" : update_post.title,
            "content": update_post.content,
            "status": update_post.status,
            "user": update_post.user.id,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=post_id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })
    from .serializers import PostSerializer
'''
'''
# 클래스형 뷰(CBV)로 구현
# APIView를 사용하기 위해 import
class PostList(APIView):
    permission_classes = [TimeAndOwnerPermission]

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 게시글 목록 불러오기
    def get(self, request, format=None):
        posts = Post.objects.all()
				# 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# 게시글 하나 불러오기
class PostDetail(APIView):
    permission_classes = [TimeAndOwnerPermission]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # 게시글 수정하기
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): # update이니까 유효성 검사 필요
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 게시글 삭제하기
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 해당 게시글에 달린 댓글 모두 조회
class CommentList(APIView):
    permission_classes = [TimeAndOwnerPermission]
    def get(self, request, post_id): # HTTP GEt 요청이 들어왔을 때 실행되는 메서드
        post = get_object_or_404(Post, pk=post_id) # Post 클래스에서 pk가 입력받은 인자와 같은 객체를 post에 담음
        comments = Comment.objects.filter(post = post) # Comment의 객체중 post_id가 입력받은 인자와 같은 객체들을 comments에 담음

        if not comments.exists(): # 댓글이 없다면 '댓글 없음' 출력
            return Response({
                "status": 200,
                "message": "댓글 없음",
                "data": []
            })
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
#S3
class ImageUploadView(APIView):
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # 동일한 파일 S3 버킷에 업로드ver
        # 파일 이름 고유화 (UUID + 확장자 유지)
        ext = image_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = f"uploads/{unique_filename}"

        # S3에 파일 저장 기본ver
        #file_path = f"uploads/{image_file.name}"

        # S3에 파일 업로드
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 업로드된 파일의 URL 생성
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"

        # DB에 저장
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)


        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''
#------------------ swagger -------------------- 
class PostList(APIView):
    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="새로운 게시글을 생성합니다.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "잘못된 요청"}
    )
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="모든 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, format=None):
        posts = Post.objects.all()
	    # 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# 게시글 하나 불러오기(swagger)
class PostDetail(APIView):
    @swagger_auto_schema(
        operation_summary="게시글 조회",
        operation_description="게시글을 조회합니다.",
        responses={200: PostSerializer}
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # 게시글 수정하기
    @swagger_auto_schema(
        operation_summary="게시글 수정",
        operation_description="게시글을 수정합니다.",
        request_body=PostSerializer,
        responses={200: PostSerializer, 400: "잘못된 요청"}
    )
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): # update이니까 유효성 검사 필요
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 게시글 삭제하기
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        operation_description="게시글을 삭제합니다.",
        responses={204: "삭제 성공", 404: "존재하지 않음"}
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 해당 게시글에 달린 댓글 모두 조회(swagger)
class CommentList(APIView):
    @swagger_auto_schema(
        operation_summary="모든 댓글 조회",
        operation_description="모든 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request, post_id): # HTTP GEt 요청이 들어왔을 때 실행되는 메서드
        post = get_object_or_404(Post, pk=post_id) # Post 클래스에서 pk가 입력받은 인자와 같은 객체를 post에 담음
        comments = Comment.objects.filter(post = post) # Comment의 객체중 post_id가 입력받은 인자와 같은 객체들을 comments에 담음

        if not comments.exists(): # 댓글이 없다면 '댓글 없음' 출력
            return Response({
                "status": 200,
                "message": "댓글 없음",
                "data": []
            })
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
# S3(swagger)
class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        operation_summary="이미지 업로드",
        operation_description="이미지를 S3에 업로드하고 URL을 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="업로드할 이미지 파일",
                type=openapi.TYPE_FILE,
                required=True
            )
        ]
    )
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # 동일한 파일 S3 버킷에 업로드ver
        # 파일 이름 고유화 (UUID + 확장자 유지)
        ext = image_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = f"uploads/{unique_filename}"

        # S3에 파일 저장 기본ver
        #file_path = f"uploads/{image_file.name}"

        # S3에 파일 업로드
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 업로드된 파일의 URL 생성
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"

        # DB에 저장
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)


        return Response(serializer.data, status=status.HTTP_201_CREATED)

#14주차 예외처리
@require_http_methods(["GET"])
def get_post_detail(reqeust, id):
    try:
        post = Post.objects.get(id=id)
        post_detail_json = {
            "id" : post.id,
            "title" : post.title,
            "content" : post.content,
            "status" : post.status,
            "user" : post.user.username
        }
        return JsonResponse({
            "status" : 200,
            "data": post_detail_json})
    except Post.DoesNotExist:
        raise PostNotFoundException
    
#댓글 생성 API
class CommentCreate(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        
        data = request.data.copy()
        data['post'] = post.id  # post 연결을 위해 명시

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)