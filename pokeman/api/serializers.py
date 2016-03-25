from rest_framework import serializers

from main.models import Vote, Answer, Post


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
