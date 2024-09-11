import json
from django.db.models import Case, When, IntegerField
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category

class ProductsList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "category",
        "stock",
    ]
    ordering_fields = ["price"]

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = queryset.annotate(
            in_stock=Case(
                When(stock__gt=0, then=1),
                default=0,
                output_field=IntegerField(),
            )
        )
        min_price = self.request.query_params.get("minPrice", None)
        max_price = self.request.query_params.get("maxPrice", None)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
            
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            return queryset.order_by("-in_stock", *ordering.split(","))
        else:
            return queryset.order_by("-in_stock")


class ProductDetail(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.prefetch_related("images"), id=product_id
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_id):
        data = json.loads(request)
        product = get_object_or_404(id=product_id)
        serializer = ProductSerializer(instance=product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product = Product.objects.get(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductByCategory(APIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filteset_fields = ["price", "stock"]

    def get(self, request, category_name):
        category = get_object_or_404(Category, name=category_name)
        products_list = Product.objects.filter(category=category)
        serializer = ProductSerializer(products_list, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data)
