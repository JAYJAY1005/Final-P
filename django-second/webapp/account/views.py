from django.contrib import auth
from django.db import connection
from django.shortcuts import render, redirect
from account.models import User
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

# password_reset_request 함수 사용을 위해 추가
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.conf import settings
from django.db.models import Q

# 로그인
def login_view(request):
    # 주소를 입력해서 들어오는 경우
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(request, userid=userid, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'message': '아이디 혹은 비밀번호가 틀렸습니다.'})
  
    
# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')
  
# 회원가입  
def signup(request):
    # 주소를 입력해서 들어오는 경우
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    elif request.method == 'POST':
        userid = request.POST['userid']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if request.POST['password'] != request.POST['password2']:
            return render(request, 'signup.html')

        user = User()
        user.new_user(userid, username, email, password)
        
        return render(request, 'login.html')


@login_required
def index(request):
    if request.user.is_superuser:
        users = get_user_model().objects.all()
        context = {
            'users':users,
        }
        return render(request, 'accounts/index.html', context)
    else:
        return redirect('articles:index')



def profile(request):
    return render(request, 'profile.html')

def userinfo(request):
    return render(request, 'userinfo.html')

# def password(request):
#     return render(request, 'password.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = get_user_model().objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = '[EMOAI] 비밀번호 재설정'
					email_template_name =  "account/password_reset_email.txt"
					c = {
						"email": user.email,
						# local: '127.0.0.1:8000', prod: 'EMO.AI.com'
						'domain': settings.HOSTNAME,
						'site_name': 'EMOAI',
						# MTE4
						"uid": urlsafe_base64_encode(force_bytes(user.pk)),
						"user": user,
						# Return a token that can be used once to do a password reset for the given user.
						'token': default_token_generator.make_token(user),
						# local: http, prod: https
						'protocol': settings.PROTOCOL,
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'ijaeyeong429@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("/password_reset_done/")
	password_reset_form = PasswordResetForm()
	return render(
		request=request,
		template_name='password_reset.html',
		context={'password_reset_form': password_reset_form})

