from django.contrib import admin
from django.urls import path,include
import blog.views

# 뭔가 수정하려고 쓴 내용


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/' , include('blog.urls') ), 
    path('', include('account.urls')),
]
