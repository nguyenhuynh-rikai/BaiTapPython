import datetime

from blog.forms import PostForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import ListView
from django.views.generic import DetailView


def hello_world(request):
    now = datetime.datetime.now()
    html = f"<html><body><h1>Bây giờ là: {now}</h1></body></html>"
    return HttpResponse(html)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list_view.html'
    context_object_name = 'posts'
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
