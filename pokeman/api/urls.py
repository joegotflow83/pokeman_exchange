from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^votes/$', views.VoteListCreateAPIView.as_view(), name='votes_api'),
    url(r'^vote/(?P<pk>\d+)/$', views.VoteRetrieveAPIView.as_view(), name='single_vote_api'),
    url(r'^answers/$', views.AnswerListCreateAPIView.as_view(), name='answers_api'),
    url(r'^answer/(?P<pk>\d+)/$', views.AnswerRetrieveUpdateAPIView.as_view(), name='single_answer_api'),
    url(r'^posts/$', views.PostListCreateAPIView.as_view(), name='posts_api'),
    url(r'^post/(?P<pk>\d+)/$', views.PostRetrieveUpdateAPIView.as_view(), name='single_post_api'),
]
