import base64
from rest_framework import serializers
from comment.serializers import CommentSerializer
from .models import Product, ProductImage, Category


def encode_image(obj):
    """
    Method to return the base64 encoding of the image.
    """
    if obj.image and hasattr(obj.image, "open"):
        with obj.image.open("rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return None


class ProductImageSerializer(serializers.ModelSerializer):
    formatted_image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "formatted_image",
        ]

    def get_formatted_image(self, obj):
        return encode_image(obj)


class ProductSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "rate",
            "price",
            "description",
            "stock",
            "comment",
            "images",
        ]


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", 'image']

    def get_image(self, obj):
        return encode_image(obj)
