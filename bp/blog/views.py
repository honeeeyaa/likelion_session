from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Comment, Like
from django.utils import timezone
# Create your views here.
def blog(request):
    blogs = Blog.objects.all()
    return render(request,'blog.html', { 'blogs' : blogs })

# R
def detail(request, blog_id):
    detail = get_object_or_404(Blog, pk=blog_id) # 글과 관련된 댓글 뭉치를 blog_id로 가져올 수 있겠구나
    comments = Comment.objects.all().filter(post = detail)

    
    # likes => 순서쌍 ('현재 blog.id','현재 user.id')
    # 이 순서쌍이 Like 모델에 있다면 좋아요를 누른 것! -> 좋아요 취소 message를 전달
    # 이 순서쌍이 Like 모델에 없다면 좋아요를 누르지 않은 것! -> 좋아요 message를 전달
    if detail.likes.filter(id = request.user.id):
        message = "좋아요 취소"

    else:
        message ="좋아요"

    return render(request ,'detail.html', 
    { 'detail' : detail, 
    'comments' : comments, 
    'message': message } ) # 여기 comments는 detail에서 for comment in comments로 쓰임


def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = "NoTitle"  # 내용 채우기
    if request.GET['title']:
        blog.title=request.GET['title']
    blog.body = request.GET['body'] # 내용 채우기
    blog.writer = request.user # 현재 user객체가 담긴다.
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.save() # 객체 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

#삭제
def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/blog/')
#update

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk =blog_id)

    if request.method == "POST":
        if request.POST['title']:
            blog.title=request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/blog/' +str(blog.id))
    else:
        return render(request,'update.html')


#comment
def comment(request,blog_id):
    if request.method == "POST" :   # post 로 왔을때 아래 실행
        comment = Comment()
        comment.body = request.POST['body']
        comment.pub_date = timezone.datetime.now()
        comment.writer = request.user
        comment.post = get_object_or_404(Blog, pk = blog_id)
        comment.save()

        return redirect('/blog/'+str(blog_id))
    else:
        return redirect('/blog/'+str(blog_id))


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    blog_id = comment.post.id               # 블로그 아이디 받아오기
    comment.delete()

    return redirect('/blog/'+str(blog_id))


# like 관련 함수

# 좋아요 누르면 실행
def post_like(request,blog_id):
    blog = get_object_or_404(Blog, pk= blog_id)
    user = request.user # 현재 객체의 유저

    if blog.likes.filter(id = user.id):
        blog.likes.remove(user) # user.id랑 같은게 있으면 좋아요 누른거니까 현재 user 정보 삭제

    else:
        blog.likes.add(user)    # user.id 없으면 좋아요 안누른거니까 user 정보 추가

    return redirect('/blog/'+str(blog_id))
