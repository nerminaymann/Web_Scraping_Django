from django.db import models

class AbstractProduct(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField(max_length=500, null=True, blank=True)
    new_price = models.CharField(max_length=100)
    old_price = models.CharField(max_length=100, null=True, blank=True)
    discount = models.CharField(max_length=50, null=True, blank=True)
    ratings = models.FloatField(default=0.0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Implement custom save behavior
        self.new_price = self.new_price.replace('EGP', '').strip()
        if self.old_price:
            self.old_price = self.old_price.replace('EGP', '').strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.new_price}"


class Product(AbstractProduct):
    def save(self, *args, **kwargs):
        if not self.old_price:
            self.discount = None
        else:
            try:
                old_price_value = float(self.old_price.replace(',', ''))
                new_price_value = float(self.new_price.replace(',', ''))
                discount_percentage = ((old_price_value - new_price_value) / old_price_value) * 100
                self.discount = f"{discount_percentage:.1f}%"
            except ValueError:
                self.discount = None

        super().save(*args, **kwargs)