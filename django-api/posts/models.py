from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile


# 게시글 모델 설정
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,) # 저자
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,) # 프로파일
    title = models.CharField(max_length=128) # 제목
    category = models.CharField(max_length=128) # 카테고리 본문
    body = models.TextField() # 글써진 공간
    image = models.ImageField(upload_to='post/', default='default.png') # 이미지
    published_date = models.DateTimeField(default=timezone.now) # 글이 올라간 시간

# 댓글 모델 설정
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    text = models.TextField()