import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author__id',
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorite = django_filters.BooleanFilter(
        method='get_is_favorite',
    )
    is_in_cart = django_filters.BooleanFilter(
        method='get_is_in_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'author', 'tag', 'is_favorite', 'is_in_cart'
        )

    def get_is_favorite(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset.all()
