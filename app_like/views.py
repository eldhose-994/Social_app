import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_like.models import Reaction, TagWeight, Post
from app_like.serializers import PostSerializer, ImagePostSerializer, ReactionSerializer, TagSerializer, \
    PostListSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class PostViewSet(PageNumberPagination, viewsets.ViewSet):
    """
    List all post & create a new s.
    """
    permission_classes = [IsAuthenticated, ]

    # serializer_class = PostListSerializer
    # pagination_class =
    # queryset = Post.objects.all()

    def get_queryset(self):
        if self.request.GET.get('recommended') == 'True':
            post_reactions = Reaction.objects.filter(user=self.request.user, reaction="Like").values_list('post')
            tags = TagWeight.objects.filter(post__in=post_reactions).order_by('-weight').values_list('tag').distinct()
            post_tags = TagWeight.objects.filter(tag__in=tags).values_list('post').order_by('-weight')
            posts = Post.objects.filter(id__in=post_tags)
            post_list = []
            # post_ids =list(set(list(post_tags)))
            for id in list(post_tags):
                post_by_id = Post.objects.get(id=id[0])
                if post_by_id in post_list:
                    pass
                else:
                    post_list.append((post_by_id))

            return post_list

        return Post.objects.all()

    def list(self, request, format=None):

        posts = self.get_queryset()
        # posts = Post.objects.all()

        paginator = Paginator(posts, 5)
        page = request.GET.get('page')

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        serializer = PostListSerializer(post, context={'request': request}, many=True)
        return Response(serializer.data)

        # return self.get_paginated_response(serializer.data)

    def create(self, request, format=None):

        data = request.data['data']
        data_json = json.loads(data)
        post_data = {
            'title': data_json['title'],
            'description': data_json['description'],
            # 'created_by': request.user,
            'published_date_time': data_json['published_date_time']
        }
        tags = data_json['tag']
        images = request.data.getlist('image')
        image_dict = []
        for i in images:
            img = {}
            img['image'] = i
            image_dict.append(img)

        serializer = PostSerializer(data=post_data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            post = serializer.save()
            serializer_image = ImagePostSerializer(data=image_dict, context={'post': post}, many=True)
            if serializer_image.is_valid(raise_exception=True):
                serializer_image.save()

            serializer_tag = TagSerializer(data=tags, context={'post': post}, many=True)
            if serializer_tag.is_valid(raise_exception=True):
                serializer_tag.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactionPostView(viewsets.ViewSet):

    def list(self, request, format=None):
        like_or_dislike = Reaction.objects.all()
        serializer = ReactionSerializer(like_or_dislike, many=True)
        return Response(serializer.data)

    def create(self, request, format=None):
        serializer = ReactionSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
