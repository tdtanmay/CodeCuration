from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='Post_List'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.contact_us, name='contact'),
    url(r'^post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<slug>[-\w]+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<slug>[-\w]+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<slug>[-\w]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<slug>[-\w]+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<slug>[-\w]+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.list_post_by_category, name='list_post_by_category'),
]
