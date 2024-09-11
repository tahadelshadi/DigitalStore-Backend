from django.db import models

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stock__gt = 0)