
import json
from django.db.models import Case, When, IntegerField
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category


class RecommendedProduct(APIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filteset_fields = ["price", "stock"]

    def get(self, request):
        # category = get_object_or_404(Category, name=category_name)
        # products_list = Product.objects.filter(category=category)
        products = Product.objects.filter(rate__gt=4)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductsList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["stock"]
    ordering_fields = ["price"]

    def get_queryset(self):
        queryset = self._get_base_queryset()

        # Filter by category name
        category_name = self.request.query_params.get("category")
        if category_name:
            queryset = self._filter_by_category(queryset, category_name)

        # Filter by price range
        min_price = self.request.query_params.get("minPrice")
        max_price = self.request.query_params.get("maxPrice")
        queryset = self._filter_by_price(queryset, min_price, max_price)

        # Apply ordering with custom stock priority
        ordering = self.request.query_params.get("ordering")
        return self._apply_ordering(queryset, ordering)

    def _get_base_queryset(self):
        """Base queryset with 'in_stock' annotation."""
        return Product.objects.annotate(
            in_stock=Case(
                When(stock__gt=0, then=1), default=0, output_field=IntegerField()
            )
        )

    def _filter_by_category(self, queryset, category_name):
        """Filter products by category name."""
        category = get_object_or_404(Category, name__iexact=category_name)
        return queryset.filter(category=category)

    def _filter_by_price(self, queryset, min_price, max_price):
        """Filter products by min and max price range."""
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    def _apply_ordering(self, queryset, ordering):
        """Apply ordering with 'in_stock' priority."""
        if ordering:
            return queryset.order_by("-in_stock", *ordering.split(","))
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
