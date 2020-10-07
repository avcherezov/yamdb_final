from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters, generics, permissions, status, viewsets

from .filters import CategoryFilter, GenreFilter, TitleFilter
from .models import Category, Comments, CustomUser, Genre, Reviews, Title
from .permissions import (IsAdmin, IsAdminOrReadOnlyPermission, IsModerator,
                          IsUser, UserRolePermissions)
from .serializers import (CategorySerializer, CommentsSerializer,
                          CostomAuthTokenSerializer, CustomUserSerializer,
                          GenreSerializer, ReviewsSerializer, TitleSerializer)
from .tokens import generation_code


class UserAdminView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdmin]


class UserViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return self.queryset.get(username=self.kwargs['username'])


class UserMeViewSet(generics.RetrieveUpdateAPIView, generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user


class CodeUserList(APIView):
    permission_classes = [permissions.AllowAny]

    @cache_page(600, cache='default', key_prefix='')
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = generation_code()
            send_mail(
                'Your confirmation code',
                'Your confirmation code',
                'admin@admin.com',
                ['anonymaususer@user.com'],
                fail_silently=False,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(TokenObtainPairView):
    queryset = CustomUser.objects.all()
    serializer_class = CostomAuthTokenSerializer
    permission_classes = [permissions.AllowAny]


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserRolePermissions]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        if Reviews.objects.filter(author=self.request.user, 
                                title_id=title_id).exists():
            raise ParseError
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserRolePermissions]

    def get_queryset(self):
        review = get_object_or_404(
            Reviews,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_class = TitleFilter


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_class = GenreFilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_class = CategoryFilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
