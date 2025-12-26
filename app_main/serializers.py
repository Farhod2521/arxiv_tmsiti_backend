from rest_framework import serializers
from .models import User, BigCategory, Category, Doc, Role

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()




class DocSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )

    class Meta:
        model = Doc
        fields = ['id', 'title', 'file', 'category', 'create_at']
        extra_kwargs = {
            'category': {'required': False}
        }


class CategorySerializer(serializers.ModelSerializer):
    docs = DocSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "ichki_raqam",
            "tartib_raqami",
            "izoh",
            "order",
            "docs"
        ]

class CategoryCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'big_category', 'ichki_raqam', 'tartib_raqami', 'izoh', 'order']
        extra_kwargs = {
            'big_category': {'required': True}
        }


class BigCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = BigCategory
        fields = ["id", "title", "categories"]

    def get_categories(self, obj):
        categories = obj.categories.all().order_by("order")
        return CategorySerializer(categories, many=True).data




class CategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['ichki_raqam', 'tartib_raqami', 'izoh', 'order']

class BigCategorySerializer1(serializers.ModelSerializer):
    categories = CategorySerializer1(many=True, read_only=True)
    
    class Meta:
        model = BigCategory
        fields = ['title', 'categories']

class RoleSerializer(serializers.ModelSerializer):
    big_categories = BigCategorySerializer1(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['name', 'big_categories']