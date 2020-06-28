from rest_framework import serializers

from app_like.models import Post, PostImages, Reaction, Tag, TagWeight


class PostSerializer(serializers.Serializer):
    # id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    # tag = TagSerializer()

    published_date_time = serializers.DateTimeField()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('email', instance.user)
        instance.description = validated_data.get('content', instance.description)
        instance.tag = validated_data.get('created', instance.tag)
        return instance


class ImagePostSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):
        validated_data['post'] = self.context['post']
        return PostImages.objects.create(**validated_data)


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.IntegerField()

    def create(self, validated_data):
        validated_data['post'] = self.context['post']
        validated_data['tag'], created = Tag.objects.get_or_create(name=validated_data.pop('name'))

        return TagWeight.objects.create(**validated_data)


class PostListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)

    published_date_time = serializers.DateTimeField()
    likes_count = serializers.SerializerMethodField(source='get_likes_count')
    dislikes_count = serializers.SerializerMethodField(source='get_dislikes_count')
    reaction = serializers.SerializerMethodField(source='get_reaction')
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        likes_count = Reaction.objects.filter(reaction='Like', post=obj).count()
        return likes_count

    def get_dislikes_count(self, obj):

        dislikes_count = Reaction.objects.filter(reaction='Dislike', post=obj).count()
        return dislikes_count

    def get_reaction(self, obj):
        try:
            reaction = obj.get_all_post_reaction.get(user=self.context['request'].user).reaction
        except Reaction.DoesNotExist:
            return 'Not Reacted'
        return reaction

    def get_images(self, obj):
        images_obj = obj.get_all_posted_images.all()
        images = ImageListSerializer(images_obj, many=True)
        return images.data
        # return [img.image.url for img in images_obj]

    def get_tags(self, obj):

        return [tag.tag.name for tag in obj.get_all_post_tags.all()]


class ImageListSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ReactionSerializer(serializers.Serializer):
    post = serializers.CharField()
    reaction = serializers.CharField()

    def create(self, validate_data):
        validate_data['post'] = Post.objects.get(id=validate_data['post'])
        validate_data['user'] = self.context['request'].user
        try:
            obj = Reaction.objects.get(user=validate_data['user'], post=validate_data['post'])
            obj.reaction = validate_data['reaction']
            return obj
        except Reaction.DoesNotExist:
            return Reaction.objects.create(**validate_data)
