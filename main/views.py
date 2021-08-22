from django.shortcuts import render

from datetime import timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .serializers import *
from .permissions import IsOwnerOrReadOnly


class PaginationClassFour(PageNumberPagination):
    page_size = 4


class PaginationClassTen(PageNumberPagination):
    page_size = 10


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    pagination_class = PaginationClassFour

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = self.request.query_params.get('filter')
        if filter == 'new':
            news_posts = timezone.now() - timedelta(days=1)
            queryset = queryset.filter(created_date__gte=news_posts)
        elif filter == 'rating':
            queryset = queryset.annotate(ratings_avg=Avg('ratings')).filter(ratings_avg__gte=7)
        return queryset


class CommentViewSet(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    pagination_class = PaginationClassTen

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    pagination_class = PaginationClassTen

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    pagination_class = PaginationClassTen

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SearchListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('query', None)

        if query:
            queryset = queryset.filter(Q(title__icontains=query) |
                                       Q(text__icontains=query) |
                                       Q(author__icontains=query))
        elif query is None:
            queryset = ''
        else:
            raise APIException('Parameter passed empty.')

        return queryset


class FavoritesViewSet(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    pagination_class = PaginationClassFour

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)