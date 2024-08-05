from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 사용자 모델을 관리하는 커스텀 매니저
class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # 이메일 주소를 표준 형식으로 정규화
        user = self.model(email=email, username=username, **extra_fields)  # 사용자 인스턴스 생성
        user.set_password(password)  # 비밀번호 설정
        user.save(using=self._db)  # 데이터베이스에 저장
        return user

    # 관리자(superuser) 사용자 생성 메서드
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # 관리자 권한 부여
        extra_fields.setdefault('is_superuser', True)  # 슈퍼유저 권한 부여
        return self.create_user(email, username, password, **extra_fields)

# 사용자 모델 정의
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # 고유한 이메일 필드
    username = models.CharField(max_length=150, unique=True)  # 고유한 사용자 이름 필드
    is_active = models.BooleanField(default=True)  # 활성 상태 필드
    is_staff = models.BooleanField(default=False)  # 스태프 권한 필드

    objects = UserManager()  # 커스텀 사용자 매니저 설정

    USERNAME_FIELD = 'email'  # 사용자 모델의 고유 식별자로 이메일 사용
    REQUIRED_FIELDS = ['username']  # 필수 입력 필드로 사용자 이름 지정

    def __str__(self):
        return self.username  # 객체를 문자열로 표현할 때 사용자 이름 반환

# 게시글 모델 정의
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 게시글 작성자와의 관계 정의
    title = models.CharField(max_length=200)  # 게시글 제목 필드
    content = models.TextField()  # 게시글 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각 자동 저장
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # 수정 시각 자동 갱신
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # 이미지 필드 (선택 사항)

    def like_count(self):
        return self.likes.count()  # 게시글의 좋아요 개수 반환

    def __str__(self):
        return self.title  # 객체를 문자열로 표현할 때 게시글 제목 반환

# 댓글 모델 정의
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 게시글과의 관계 정의
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 댓글 작성자와의 관계 정의
    content = models.TextField()  # 댓글 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각 자동 저장

    def __str__(self):
        return self.content[:20]  # 객체를 문자열로 표현할 때 댓글 내용의 앞 20자 반환

    def like_count(self):
        return self.likes.count()  # 댓글의 좋아요 개수 반환

# 좋아요 모델 정의
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  # 게시글과의 관계 정의
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와의 관계 정의
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각 자동 저장

    class Meta:
        unique_together = (('user', 'post'),)  # 같은 사용자가 같은 게시글에 여러 번 좋아요를 할 수 없도록 설정

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'  # 객체를 문자열로 표현할 때 "사용자 likes 게시글 제목" 반환
