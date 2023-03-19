from rest_framework import serializers
from .models import Post
from users.serializers import ProfileSerializer

# 각자 용도가 다르기에 시리얼라이저가 두개 필요함


class PostSerializer(serializers.ModelSerializer):
    # 프로파일 필드를 따로 코드로 정의해주는 이유는 작성하지 않을시 프로파일의 pk 값만을 나타내게 됨 
    # 해당글의 작성자 실제 프로필을 알고 싶은것이기에 
    # 이렇게 시리얼라이저 내에 또 다른 시리얼라이져를 넣어 이중으로 연결구조로 작성 - nested serializer
    profile = ProfileSerializer(read_only=True)  

    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "comments")


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "category", "body", "image")