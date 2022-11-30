from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
# from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_list(request,tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts,'tag':tag})


def post_detail(request, year,month,day,post):
    # try:
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,publish__year=year,publish__month=month,publish__day=day,slug=post)
    # Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Posts Found.")

    comments = post.comments.filter(active=True)
    form = CommentForm()

    #similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,'form':form,'comments':comments,'similar_posts':similar_posts})

def post_share(request,post_id):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,id=post_id)
    sent=False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = post.get_absolute_url()
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments : {cd['comments']}"
            send_mail(subject,message,'hanzawnyineonline@gmail.com',[cd['to']])
            sent=True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
        {'post': post,
        'form': form,
        'comment': comment})


# from django.views.generic import ListView

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name='posts'
#     paginate_by: int=1
#     template_name: str='blog/post/list.html'
