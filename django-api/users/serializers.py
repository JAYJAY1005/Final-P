# view 가 아닌 serializers 로 회원가입 기능 구현
# 회원가입 프로세스
# 1. 사용자가 정해진 폼에 따라 데이터를 입력함. (username, email, password, password2)
# 2. 해당 데이터가 들어오면 ID가 중복되지는 않는지 ,비밀번호가 너무 짧거나 쉽지는 않은지 검사한다.
# 3. 2단계를 통과했다면 회원을 생성한다.
# 4. 회원 생성이 완료되면 해당 회원에 대한 토큰을 생성한다.
 
from django.contrib.auth.models import User # 장고에서 제공하는 기본 User 모델
from django.contrib.auth.password_validation import validate_password # Django의 기본 패스워드 검증 도구  
from rest_framework import serializers
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구
from rest_framework.authtoken.models import Token # Token 모델
from django.contrib.auth import authenticate # Django의 기본 authenticate 함수, 우리가 설정한 DefaultAuthBackend인 TokenAuth 방식으로
                                             # 유저를 인정해줌
from .models import Profile                  

class RegisterSerializer(serializers.ModelSerializer): # 회원 가입 시리얼라이저
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인을 위한 필드

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data): # 추가적으로 비밀번호 일치 여부를 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data

    def create(self, validated_data): # create 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
# write_only 옵션을 통해 클라이언트 -> 서버 방향의 역직렬화는 가능,서버 -> 클라이언트 방향의 직렬화는 불가능

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 토큰에서 유저 찾아 응답
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", "subjects")
