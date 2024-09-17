from django.db import models
from products.models import Product
from user.models import User


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='comment', on_delete=models.CASCADE)
    context = models.TextField()
    rate = models.DecimalField(
        default=1, max_length=5, max_digits=5, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment for {self.product.name} from {self.user.first_name}{self.user.last_name}'
    