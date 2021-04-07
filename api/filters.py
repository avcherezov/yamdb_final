from django_filters import rest_framework as filters

from .models import Title, Genre, Category


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug")
    genre = filters.CharFilter(field_name="genre__slug")
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year', 'genre', 'name', 'category']


class GenreFilter(filters.FilterSet):

    class Meta:
        model = Genre
        fields = ['name']


class CategoryFilter(filters.FilterSet):

    slug = filters.CharFilter()

    class Meta:
        model = Category
        fields = ['name']
