from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from .serializers import PostSerializer, VoteSerializer, AnswerSerializer
from main.models import Post, Vote, Answer


class PostListCreateAPIView(generics.ListCreateAPIView):
    """Display posts endpoint"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)


class PostRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Allow a user to put and patch endpoint"""
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return Post.objects.get(Q(pk=self.kwargs['pk']), Q(user=self.request.user))


class VoteListCreateAPIView(generics.ListCreateAPIView):
    """Display votes endpoint"""
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class VoteRetrieveAPIView(generics.RetrieveAPIView):
    """Display a single post endpoint"""
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return Vote.objects.get(pk=self.kwargs['pk'])


class AnswerListCreateAPIView(generics.ListCreateAPIView):
    """Display answer endpoint"""
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        request.data['data'] = request.user.pk
        return super().create(request, *args, **kwargs)


class AnswerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Display a single post endpoint"""
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return Answer.objects.get(Q(pk=self.kwargs['pk']), Q(user=self.request.user))

