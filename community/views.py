from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def post_list(request):
    """
    게시글 목록을 가져오는 뷰
    - GET 요청을 처리하며, 모든 게시글을 조회하여 JSON 형태로 반환합니다.
    """
    posts = Post.objects.all()  # 모든 게시글을 가져옴
    serializer = PostSerializer(posts, many=True)  # 여러 개의 게시글을 직렬화
    return Response(serializer.data)  # 직렬화된 데이터를 JSON 형태로 반환

@api_view(['GET'])
def post_detail(request, pk):
    """
    특정 게시글의 세부 정보를 가져오는 뷰
    - GET 요청을 처리하며, 주어진 ID에 해당하는 게시글의 세부 정보를 반환합니다.
    """
    post = get_object_or_404(Post, id=pk)  # ID에 해당하는 게시글을 조회, 없으면 404 오류
    serializer = PostSerializer(post)  # 게시글을 직렬화
    return Response(serializer.data)  # 직렬화된 데이터를 JSON 형태로 반환

@api_view(['POST'])
def post_create(request):
    """
    새로운 게시글을 생성하는 뷰
    - POST 요청을 처리하며, 요청 본문에 포함된 데이터로 새로운 게시글을 생성합니다.
    """
    user_data = request.data.pop('author')  # 요청 본문에서 사용자 데이터를 추출
    user_serializer = UserSerializer(data=user_data)  # 사용자 데이터를 직렬화
    
    if user_serializer.is_valid():  # 사용자 데이터 유효성 검사
        user = user_serializer.save()  # 유효하다면 사용자 저장
        post_serializer = PostSerializer(data=request.data)  # 나머지 요청 데이터를 직렬화
        if post_serializer.is_valid():  # 게시글 데이터 유효성 검사
            post = post_serializer.save(author=user)  # 유효하다면 게시글 생성, 작성자 설정
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)  # 생성된 게시글 데이터를 JSON 형태로 반환
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 게시글 데이터 유효성 검사 실패 시 오류 반환
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 사용자 데이터 유효성 검사 실패 시 오류 반환

@api_view(['DELETE'])
def post_delete(request, post_id):
    """
    특정 게시글을 삭제하는 뷰
    - DELETE 요청을 처리하며, 주어진 ID에 해당하는 게시글을 삭제합니다.
    """
    post = get_object_or_404(Post, id=post_id)  # ID에 해당하는 게시글을 조회, 없으면 404 오류
    post.delete()  # 게시글 삭제
    return Response(status=status.HTTP_204_NO_CONTENT)  # 성공적으로 처리되었음을 나타내는 상태 코드 반환

@api_view(['POST'])
def add_comment(request, pk):
    """
    특정 게시글에 댓글을 추가하는 뷰
    - POST 요청을 처리하며, 요청 본문에 포함된 데이터로 해당 게시글에 댓글을 추가합니다.
    """
    post = get_object_or_404(Post, id=pk)  # ID에 해당하는 게시글을 조회, 없으면 404 오류
    user_data = request.data.pop('author')  # 요청 본문에서 사용자 데이터를 추출
    user_serializer = UserSerializer(data=user_data)  # 사용자 데이터를 직렬화
    
    if user_serializer.is_valid():  # 사용자 데이터 유효성 검사
        user = user_serializer.save()  # 유효하다면 사용자 저장
        comment_serializer = CommentSerializer(data=request.data)  # 나머지 요청 데이터를 직렬화
        if comment_serializer.is_valid():  # 댓글 데이터 유효성 검사
            comment = comment_serializer.save(author=user, post=post)  # 유효하다면 댓글 생성, 작성자와 게시글 설정
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)  # 생성된 댓글 데이터를 JSON 형태로 반환
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 댓글 데이터 유효성 검사 실패 시 오류 반환
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 사용자 데이터 유효성 검사 실패 시 오류 반환

@api_view(['POST'])
def like_post(request, pk):
    """
    특정 게시글에 좋아요를 추가하거나 제거하는 뷰
    - POST 요청을 처리하며, 요청 본문에 포함된 데이터로 해당 게시글에 좋아요를 추가하거나 기존 좋아요를 제거합니다.
    """
    post = get_object_or_404(Post, id=pk)  # ID에 해당하는 게시글을 조회, 없으면 404 오류
    user_data = request.data.pop('user')  # 요청 본문에서 사용자 데이터를 추출
    user_serializer = UserSerializer(data=user_data)  # 사용자 데이터를 직렬화
    
    if user_serializer.is_valid():  # 사용자 데이터 유효성 검사
        user = user_serializer.save()  # 유효하다면 사용자 저장
        like, created = Like.objects.get_or_create(post=post, user=user)  # 게시글과 사용자로 좋아요 객체를 조회하거나 생성
        if not created:  # 이미 좋아요가 존재하는 경우
            like.delete()  # 좋아요를 제거
        return Response(status=status.HTTP_204_NO_CONTENT)  # 성공적으로 처리되었음을 나타내는 상태 코드 반환
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 사용자 데이터 유효성 검사 실패 시 오류 반환

@api_view(['DELETE'])
def comment_delete(request, comment_id):
    """
    특정 댓글을 삭제하는 뷰
    - DELETE 요청을 처리하며, 주어진 ID에 해당하는 댓글을 삭제합니다.
    """
    comment = get_object_or_404(Comment, id=comment_id)  # ID에 해당하는 댓글을 조회, 없으면 404 오류
    comment.delete()  # 댓글 삭제
    return Response(status=status.HTTP_204_NO_CONTENT)  # 성공적으로 처리되었음을 나타내는 상태 코드 반환
