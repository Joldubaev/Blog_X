from django.db.models import Q, Avg
from rest_framework import serializers
from rest_framework.utils import json

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)
    update_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'text', 'image', 'author', 'created_date', 'update_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data

        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['category'] = instance.category.name
            representation['text'] = instance.text[:30] + '...' if len(instance.text) >=30 else instance.text
            representation['comments'] = instance.comments.count()
            representation['ratings'] = instance.ratings.aggregate(Avg('grade'))
            representation['likes'] = instance.likes.filter(status=True).count()
            representation['dislikes'] = instance.likes.filter(status=False).count()

        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            representation['ratings'] = RatingSerializer(instance.ratings.all(),
                                                        many=True).data
            representation['ratings_avg'] = instance.ratings.aggregate(Avg('grade'))

            representation['likes'] = LikeSerializer(instance.likes.all(),
                                                         many=True).data

            representation['likes_count'] = instance.likes.filter(status=True).count()
            representation['dislikes_count'] = instance.likes.filter(status=False).count()

        return representation


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = ('id', 'author', 'post', 'grade')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Rating.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('This user has already rate this post.')

        rating = Rating.objects.create(
            **validated_data
        )

        return rating


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment', 'author', 'created_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['post'] = instance.post.title
            representation['comment'] = instance.comment[:20] + '...' if len(instance.comment) >=20 else instance.comment

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = ('id', 'post', 'author', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Like.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('This user has already liked this post..')

        like = Like.objects.create(
            **validated_data
        )

        return like


class FavoritesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'post', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Favorites.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('This post has already been added to favorites.')

        favorites = Favorites.objects.create(
            **validated_data
        )

        return favorites