from django.conf.urls import url
from django.views.decorators.http import require_POST

from main import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^create/post/$', views.CreateQuestion.as_view(), name='create_post'),
    url(r'^questions/$', views.ListQuestions.as_view(), name='questions_list'),
    url(r'^question/(?P<pk>\d+)/$', views.QuestionDetail.as_view(), name='question_detail'),
    url(r'^create/answer/(?P<pk>\d+)/$', require_POST(views.CreateAnswer.as_view()), name='create_answer'),
    url(r'^upvote/(?P<pk>\d+)/(?P<answer_id>\d+)/$', views.UpVote.as_view(), name='upvote'),
    url(r'^downvote/(?P<pk>\d+)/(?P<answer_id>\d+)/$', views.DownVote.as_view(), name='downvote'),
    url(r'^delete/post/(?P<pk>\d+)/$', views.DeleteQuestion.as_view(), name='delete_question'),
    url(r'^pokemon/search/$', views.Pokemon.as_view(), name='pokemon_search'),
    url(r'^search/question/$', views.SearchQuestion.as_view(), name='search_question'),
    url(r'^charge/$', views.Charge.as_view(), name='charge'),
]
