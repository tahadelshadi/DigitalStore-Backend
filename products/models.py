from django.db import models
from .managers import ProductManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Category


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.id} {self.name}"

# Product


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    # slug = models.SlugField(max_length=200,unique=True)
    stock = models.PositiveIntegerField(default=0)
    rate = models.DecimalField(
        default=1, max_length=5, max_digits=10, decimal_places=1)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    available = ProductManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product/")
    formatted_image = ImageSpecField(source='image',
                                     processors=[ResizeToFill(500, 500)],
                                     format='WEBP',
                                     options={'quality': 80})
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"


# Orders
class Order(models.Model):
    address = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return "{}".format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{}".format(self.id)
