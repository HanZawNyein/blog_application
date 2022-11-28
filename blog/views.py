from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,1)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year,month,day,post):
    # try:
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,publish__year=year,publish__month=month,publish__day=day,slug=post)
    # Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Posts Found.")
    return render(request, 'blog/post/detail.html', {'post': post})
