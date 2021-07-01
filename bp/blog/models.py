from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('data published')
    body = models.TextField()

    writer = models.ForeignKey(User,on_delete=models.CASCADE, null=True) #user를 블로그에 일대다로 연결해준다(n:블로그->1)
                                                                        # 정보 없어도 ㄱㅊ: null허용
    
    likes = models.ManyToManyField(User, through='Like', through_fields=('blog','user'), related_name='likes')
         # like 를 통해(아래 만든거) # blog랑 user를 통해 하겠다.    # blog랑 user사이 중계모델을 만드는데, 그게 like이고, 다대다 모델로 쓰겠다!

    def __str__(self):
        return self.title



# 댓글
class Comment(models.Model):
    body = models.TextField(max_length=500)
    pub_date = models.DateTimeField('data published')

    # 아래가 keypoint
    writer = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자만 삭제가능
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)   # blog 하나당 댓글 여러개 가능하도록 


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # like 입장에서는 유저에 대해서는 1:N , blog에 대해서는 M:1 따라서 foreign key 사용

