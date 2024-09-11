import base64
from rest_framework import serializers
from .models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
        ]

    def get_image(self, obj):
        """
        Method to return the base64 encoding of the image.
        """
        if obj.image and hasattr(obj.image, "open"):
            with obj.image.open("rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "rate",
            "price",
            "description",
            "images",
            "stock",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
