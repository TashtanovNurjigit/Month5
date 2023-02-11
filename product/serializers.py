from rest_framework import serializers
from .models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tag_list = serializers.SerializerMethodField()
    product_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id product_reviews rating title price product_quantity category tag_list'.split()

    def get_tag_list(self, product_object):
        return [i.name for i in product_object.tags.all()]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title category rating tags price product_quantity created updated is_active text'.split()


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1)
    price = serializers.FloatField(min_value=1, max_value=1000000)
    quantity = serializers.IntegerField(default=0)
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(
        min_value=1
    ))

    def validate_category_id(self, category_id):  # 100
        # try:
        #     Category.objects.get(id=category_id)
        # except Category.DoesNotExist:
        #     raise ValidationError(f'Category with ({category_id}) does not exists!')
        # return category_id
        categories = Category.objects.filter(id=category_id)
        if categories.count() == 0:
            raise ValidationError(f'Category with ({category_id}) does not exists!')
        return category_id

    def validate_tags(self, tags):
        tags_id = [i[0] for i in Tag.objects.all().values_list('id')]
        for t in tags:
            if t not in tags_id:
                raise ValidationError(f'Tag with ({t}) does not exists!')
        return tags