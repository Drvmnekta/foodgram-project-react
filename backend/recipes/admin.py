from django.contrib import admin

from .models import (Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag,
                     TagRecipe)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-empty-'


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


class TagRecipeInLine(admin.TabularInline):
    model = TagRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, TagRecipeInLine,)
    list_display = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = (
        'name',
        'author',
        'cooking_time',
    )
    empty_value_display = '-empty-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    empty_value_display = '-empty-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-empty-'
