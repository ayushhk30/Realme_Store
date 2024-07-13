from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mobile(models.Model):
    image = models.ImageField(upload_to='mobile/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    colors= models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    colors= models.CharField(max_length=255)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    mobile = models.ForeignKey(Mobile, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}"

    def get_item_name(self):
        if self.mobile:
            return self.mobile.name
        return self.product.name
    
    @property
    def total(self):
        if self.product:
            return self.product.price * self.quantity
        if self.mobile:
            return self.mobile.price * self.quantity
        return 0