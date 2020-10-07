from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Category, Comments, CustomUser, Genre, Reviews, Title


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'role',
            'email',
        )


class CostomAuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label=_("email"))

    class Meta:
        model = CustomUser
        fields = ('email', 'confirme_code',)

    def validate(self, data):
        email = self.initial_data['email']
        confirme_code = data['confirme_code']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if confirme_code == user.confirme_code:
                user.is_active = True
                user.save()
                refresh = TokenObtainPairSerializer.get_token(user)
                del data['email']
                del data['confirme_code']
                data['token'] = str(refresh.access_token)
                return data
        else:
            raise serializers.ValidationError(
                                {'token': 'User already has token.'})


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comments


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}

    def to_internal_value(self, data):
        category = Category.objects.get(slug=data)
        return category


class GenreSlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}

    def to_internal_value(self, data):
        genre = Genre.objects.get(slug=data)
        return genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False
    )
    category = CategorySlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
    rating = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        fields = (
            'id',
            'category',
            'genre',
            'name',
            'year',
            'rating',
            'description'
        )
        model = Title
        