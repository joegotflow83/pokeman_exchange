from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse

from .models import Post, Answer, Vote
from .forms import AnswerForm


class Home(TemplateView):
    """Users home page"""
    template_name = 'main/home.html'


class CreateQuestion(CreateView):
    """Allow user to create a question"""
    model = Post
    fields = ('title', 'body', 'tags')

    def form_valid(self, form):
        """Validate the form"""
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()
        user = self.request.user
        user.userprofile.score += 5
        user.userprofile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class ListQuestions(ListView):
    """List all questions"""
    model = Post


class QuestionDetail(DetailView):
    """View a question in detail"""
    model = Post

    def get_context_data(self, **kwargs):
        """Display answer form for users to answer questions"""
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerForm
        return context


class CreateAnswer(CreateView):
    """Allow a user to answer a question"""
    model = Answer
    fields = ('response',)

    def form_valid(self, form):
        """Validate the form"""
        new_answer = form.save(commit=False)
        new_answer.user = self.request.user
        new_answer.save()
        question = Post.objects.get(pk=self.kwargs['pk'])
        question.answers.add(new_answer)
        question.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'pk': self.kwargs['pk']})


class UpVote(View):
    """Allow a user to upvote an answer"""
    def get(self, request, pk, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        url = reverse('question_detail', kwargs={'pk': self.kwargs['pk']})
        if answer.user == request.user:
            return HttpResponseRedirect(url)
        for vote in answer.votes.all():
            if vote.username == request.user.username:
                return HttpResponseRedirect(url)
        new_vote = Vote(username=request.user)
        new_vote.save()
        answer.votes.add(new_vote)
        answer.like += 1
        answer.user.userprofile.score += 10
        answer.user.userprofile.save()
        answer.save()
        return HttpResponseRedirect(url)


class DownVote(View):
    """Allow a user to downvote an answer"""
    def get(self, request, pk, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        url = reverse('question_detail', kwargs={'pk': self.kwargs['pk']})
        if answer.user == request.user:
            return HttpResponseRedirect(url)
        for vote in answer.votes.all():
            if vote.username == request.user.username:
                return HttpResponseRedirect(url)
        new_vote = Vote(username=request.user)
        new_vote.save()
        answer.votes.add(new_vote)
        answer.like -= 1
        answer.user.userprofile.score -= 5
        user = self.request.user
        user.userprofile.score -= 1
        user.userprofile.save()
        answer.user.userprofile.save()
        answer.save()
        return HttpResponseRedirect(url)
