from . import views
from django.urls import path
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('',views.PostListView.as_view(),name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list,name="post_list_by_tag"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share,name='post_share'),
    path('<int:post_id>/comment/',views.post_comment,name='post_comment'),

    #feed
    path('feed/',LatestPostFeed(),name='post_feed'),
    # https://github.com/yang991178/fluent-reader/releases/tag/v1.1.3

    path('search/',views.post_search,name='post_search')
]
