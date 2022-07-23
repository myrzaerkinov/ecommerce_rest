from rest_framework import serializers
from products.models import Product, Category, Review
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title description price category ' \
                 'review count_reviews all_reviews rating'.split()

    def get_category(self, product):
        return product.category.name

    def get_review(self, product):
        serializer = ReviewSerializer(Review.objects.filter(
            author__isnull=False, product=product), many=True)
        return serializer.data

# class ObjectCreateSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     is_active = serializers.BooleanField()

class ReviewCreateSerializer(serializers.Serializer):           #Сериализатор для фейковых комментариев
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=50)


class ProductCreateUpdateSerializer(serializers.Serializer): #Валидация через сериализаторы
    title = serializers.CharField(min_length=2, max_length=10)
    description = serializers.CharField()
    price = serializers.FloatField()
    category_id = serializers.IntegerField() #100
    reviews = serializers.ListField(child=ReviewCreateSerializer())         # Поле для валидации от сериализатора отзывов
    # list_ = serializers.ListField(child=serializers.CharField())
    # object_ = ObjectCreateSerializer()


    # def validate(self, attrs):                              #Общая валидация по всем полям моделей.
    #     id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=id)
    #     except Category.DoesNotExist:
    #         raise ValidationError(f'Category with id={id} not found!')
    #     return attrs

    def validate_category_id(self, category_id):               # Точечная валидация по конкретным полям моделей.
        if Category.objects.filter(id=category_id).count() == 0:
            raise ValidationError(f'Category with id={category_id} not found!')
        return category_id
