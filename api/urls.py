from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CodeUserList, CommentsViewSet,
                    GenresViewSet, ObtainAuthToken, ReviewsViewSet,
                    TitlesViewSet, UserAdminView, UserMeViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentsViewSet, basename='comments')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path(r'users/', UserAdminView.as_view()),
    path(r'users/me/', UserMeViewSet.as_view()),
    path(r'users/<str:username>/', UserViewSet.as_view()),
    path(r'auth/email/', CodeUserList.as_view()),
    path(r'auth/token/', ObtainAuthToken.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
