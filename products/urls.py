from django.urls import path
from .views import ProductDetail, CategoryList,ProductByCategory,ProductsList, RecommendedProduct

urlpatterns = [
    path("api/products/", ProductsList.as_view(), name="product_list"),
    path('api/products/<int:product_id>/', ProductDetail.as_view(),name='product_detail'),
    path('api/products/recommend/', RecommendedProduct.as_view(),name='product_detail'),
    path('api/category/<str:category_name>/', ProductByCategory.as_view(),name='category_detail'),
    path('api/category/', CategoryList.as_view(),name="categories_list"),
]
