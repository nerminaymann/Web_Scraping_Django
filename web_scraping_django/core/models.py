from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    new_price = models.CharField(max_length=50)
    old_price = models.CharField(max_length=50, null=True, blank=True)
    discount = models.CharField(max_length=20, null=True, blank=True)
    ratings = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.name

