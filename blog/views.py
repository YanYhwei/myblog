from django.shortcuts import render
# Create your views here.

import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post
from comments.forms import CommentsForm

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.body = markdown.markdown(post.body,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentsForm()
    # 获取这篇post下的全部评论
    comment_list = post.comments_set.all()

    # 将文章,表单,以及文章下的评论列表作为作为模板变量传给 detail.html 模板,以便渲染相应数据
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list
    }

    return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,created_time__month=month)
    return render(request,'blog/index.html',context={'post_list':post_list})
