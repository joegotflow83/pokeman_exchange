from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from rest_framework.authtoken.models import Token
import requests
import stripe

from accounts.models import UserProfile
from .models import Post, Answer, Vote
from .forms import AnswerForm


class Index(TemplateView):
    """First page of web app"""
    template_name = 'main/index.html'


class Home(TemplateView):
    """Users home page"""
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user)
        context['questions'] = Post.objects.filter(user=self.request.user)
        context['top_3'] = UserProfile.objects.order_by('-score')[:3]
        return context


class CreateQuestion(CreateView):
    """Allow user to create a question"""
    model = Post
    fields = ('title', 'body', 'tags')

    def form_valid(self, form):
        """Validate the form"""
        user_posts = Post.objects.filter(user=self.request.user)
        print(user_posts.count())
        if user_posts.count() > 3:
            return render(self.request, 'error/error.html')
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()
        user = self.request.user
        user.userprofile.score += 5
        user.userprofile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class DeleteQuestion(DeleteView):
    """Allow a user to delete their question"""
    model = Post

    def get_success_url(self):
        return reverse_lazy('home')


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


class Pokemon(TemplateView):
    """Display pokemon data"""
    template_name = 'main/pokemon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', False)
        pokemon = requests.get("http://pokeapi.co/api/v2/pokemon/{}".format(search)).json()
        context['pokemon'] = pokemon
        return context


class SearchQuestion(TemplateView):
    """Allow a user to search for a question by tags"""
    template_name = 'main/question_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('query', False)
        questions = Post.objects.filter(tags__name=search)
        context['questions'] = questions
        return context


class Charge(View):
    """Confirm charge went through"""
    def post(self, request):
        user = request.user
        user.userprofile.paid = True
        user.userprofile.save()
        stripe_keys = {
            'secret_key': 'sk_test_rt2Qf6UZcub65Rc5sdS7OPlY',
            'publishable_key': 'pk_test_u5nWdGCYlT5YVAqnf5R38cgX'
        }

        stripe.api_key = stripe_keys['secret_key']
        amount = 1000

        customer = stripe.Customer.create(
            email=request.POST["stripeEmail"],
            card=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency="usd",
            description="Unlimited Questions"
        )
        return render(request, 'main/charge.html')
