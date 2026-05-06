import datetime

from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

def hello_world(request):
    now = datetime.datetime.now()
    html = f"<html><body><h1>Bây giờ là: {now}</h1></body></html>"
    return HttpResponse(html)

def post_list(request):
    all_post = Post.objects.all().order_by('-created_at')

    context = {
        'posts': all_post,
    }

    return render(request, 'blog/post_list.html', context)