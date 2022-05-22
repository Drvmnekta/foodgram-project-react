from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe)
from users.models import Follow, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class RecipeSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'image', 'duration')


class IngredientRecipeSmallSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    units = serializers.ReadOnlyField(
        source='ingredient.units'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'units', 'amount')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed'
        )
        extra_kwargs = {'password' : {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = (make_password(validated_data.pop('password')))
        return super().create(validated_data)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            Follow.objects.filter(
                follower=request.user,
                author__id=obj.id
            ).exists()
            and request.user.is_authenticated
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserSerializer(many=False)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipe_ingredient'
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe__id=obj.id
            ).exists()
        )

    def get_is_in_cart(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Cart.objects.filter(
                user=request.user,
                recipe__id=obj.id
            ).exists()
        )


class RecipePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False
    )
    ingredients = IngredientRecipeSmallSerializer(
        source='recipe_ingredient',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    is_favorite = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe__id=obj.id
            ).exists()
        )

    def get_is_in_cart(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Cart.objects.filter(
                user=request.user,
                recipe__id=obj.id
            ).exists()
        )

    def add_tags_and_ingredients(self, tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        for ingredient in ingredients:
            if not IngredientRecipe.objects.filter(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe).exists():
                ingredient_recipe = IngredientRecipe.objects.create(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe
                )
                ingredient_recipe.amount = ingredient['amount']
                ingredient_recipe.save()
            else:
                IngredientRecipe.objects.filter(
                    recipe=recipe
                ).delete()
                recipe.delete()
                raise serializers.ValidationError(
                    'Duplicated ingredient'
                )
        return recipe

    def create(self, validated_data):
        author = validated_data.get('author')
        title = validated_data.get('title')
        image = validated_data.get('image')
        description = validated_data.get('description')
        ingredients = validated_data.pop('recipes')
        tag = validated_data.pop('tag')
        duration = validated_data.get('duration')
        pub_date = validated_data.get('pub_date')
        recipe = Recipe.objects.create(
            author=author,
            title=title,
            image=image,
            description=description,
            duration=duration,
            pub_date=pub_date,
        )
        recipe = self.add_tags_and_ingredients(tag, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipes')
        tag = validated_data.pop('tag')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance = self.add_tags_and_ingredients(
            tag, ingredients, instance
        )
        super().update(instance, validated_data)
        instance.save()
        return instance


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            Follow.objects.filter(
                follower=request.user,
                author__id=obj.id
            ).exists()
            and request.user.is_authenticated
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(suthor=obj.author)
        