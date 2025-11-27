from rest_framework import serializers
from .models import User, BigCategory, Category, Doc

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()



class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        fields = ["id", "title", "file", "category"]


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


class BigCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = BigCategory
        fields = ["id", "title", "categories"]

    def get_categories(self, obj):
        categories = obj.categories.all().order_by("order")
        return CategorySerializer(categories, many=True).data