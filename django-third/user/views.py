from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Posts, Comments
from .forms import PostsForm, CommentsForm
from django.http import HttpResponseNotAllowed,HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout,login
from django.contrib.auth.models import User

# 로그인 기능 구현
def Login(request):
    if request.method == 'GET':
        redirect('main')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.auth(email, password)

        if user is not None:
            print("인증성공")
            login(request,user)
        else:
            print("인증실패")
        
        return redirect('main')

def Logout(request):
    logout(request)
    return redirect('main')

# 회원 가입 기능 구현
def signup(request):
    data = {}
    if request.method == 'GET':
        data['page'] = '회원가입'
        return render(request, 'signup.html', data)
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        print(f'{username} {email} {password}')

        user = User()
        user.new_user(username, email, password)
        return render(request, 'main.html', data)

# 게시판 페이지 설정
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    Posts_list = Posts.objects.order_by('-create_date') # 생성한 날짜 보이기
    if kw:
        Posts_list = Posts_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(Comments__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(Comments__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(Posts_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'Posts_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'QnA/Posts_list.html', context)

def detail(request, Posts_id):
    Posts = get_object_or_404(Posts, pk=Posts_id)
    context = {'Posts': Posts}
    return render(request, 'QnA/Posts_detail.html', context)

@login_required
def Comments_create(request, Posts_id):
    """
    QnA 답변등록
    """
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            Comments = form.save(commit=False)
            Comments.author = request.user  # author 속성에 로그인 계정 저장
            Comments.create_date = timezone.now()
            Comments.Posts = Posts
            Comments.save()
            return redirect('QnA:detail', Posts_id=Posts.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'Posts': Posts, 'form': form}
    return render(request, 'QnA/Posts_detail.html', context)

@login_required
def Posts_create(request):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            Posts = form.save(commit=False)
            Posts.author = request.user  # author 속성에 로그인 계정 저장
            Posts.create_date = timezone.now()
            Posts.save()
            return redirect('QnA:index')
    else:
        form = PostsForm()
    context = {'form': form}
    return render(request, 'QnA/Posts_form.html', context)

@login_required
def Posts_modify(request, Posts_id):
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.user != Posts.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('QnA:detail', Posts_id=Posts.id)
    if request.method == "POST":
        form = PostsForm(request.POST, instance=Posts)
        if form.is_valid():
            Posts = form.save(commit=False)
            Posts.modify_date = timezone.now()  # 수정일시 저장
            Posts.save()
            return redirect('QnA:detail', Posts_id=Posts.id)
    else:
        form = PostsForm(instance=Posts)
    context = {'form': form}
    return render(request, 'QnA/Posts_form.html', context)

@login_required
def Posts_delete(request, Posts_id):
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.user != Posts.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('QnA:detail', Posts_id=Posts.id)
    Posts.delete()
    return redirect('QnA:index')

@login_required
def Comments_modify(request, Comments_id):
    Comments = get_object_or_404(Comments, pk=Comments_id)
    if request.user != Comments.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('QnA:detail', Posts_id=Comments.Posts.id)
    if request.method == "POST":
        form = CommentsForm(request.POST, instance=Comments)
        if form.is_valid():
            Comments = form.save(commit=False)
            Comments.modify_date = timezone.now()
            Comments.save()
            return redirect('QnA:detail', Posts_id=Comments.Posts.id)
    else:
        form = CommentsForm(instance=Comments)
    context = {'Comments': Comments, 'form': form}
    return render(request, 'QnA/Comments_form.html', context)

@login_required
def Comments_delete(request, Comments_id):
    Comments = get_object_or_404(Comments, pk=Comments_id)
    if request.user != Comments.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        Comments.delete()
    return redirect('QnA:detail', Posts_id=Comments.Posts.id)
