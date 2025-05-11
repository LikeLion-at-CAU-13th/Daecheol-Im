from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST", "GET"])
def post_list(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
   
        #user_id = body.get('user') 로그인 기능 추가시 해제
        #user = get_object_or_404(User, pk=user_id)
        
        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            #user = user,
            password = body['password'],
            name = body['name'],
        )
    
        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content": new_post.content,
            #"user": new_post.user.id,
            "password": new_post.password,
            "name": new_post.name,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    # 게시글 전체 조회
    if request.method == "GET":
        post_all = Post.objects.all().order_by('-created') #최신순으로 정렬
    
		# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                #"user": post.user.id,
                "password": post.password,
                "name": post.name,
                "created": post.created.strftime('%Y-%m-%d %H:%M'),
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })

@csrf_exempt
@require_http_methods(["DELETE"])
def post_delete(request, post_id):
    delete_post = get_object_or_404(Post, pk=post_id)

    body = json.loads(request.body.decode('utf-8'))
    input_password = body.get('password')  # 클라이언트가 보내는 비밀번호

    if input_password == delete_post.password:
        delete_post.delete()
        return JsonResponse({
            'status': 200,
            'message': '게시글 삭제 성공',
            'data': None
        })
    else:
        return JsonResponse({
            'status': 403,
            'message': '비밀번호가 일치하지 않습니다.',
            'data': None
        }, status=403)
    