from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Mobile(models.Model):
    image = models.ImageField(upload_to='mobile/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    colors= models.CharField(max_length=255)
    battery=models.CharField(max_length=255)
    ram=models.CharField(max_length=255)
    storage=models.CharField(max_length=255)
    camera=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    review=models.TextField()
    

    def __str__(self):
        return f"{self.name}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlist')
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    
  

    class Meta:
        unique_together = ('user', 'mobile')

User.add_to_class('wishlist', models.ManyToManyField(Mobile, through=Wishlist, related_name='wishlisted_by'))
    
class Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=255)
    mic= models.CharField(max_length=255)
    description = models.TextField()
    colors= models.CharField(max_length=255)
    range=  models.CharField(max_length=255)
    battery= models.CharField(max_length=255)
    bluetooth= models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    review=models.TextField()

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
    
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def total_cost(self):
        return sum(item.price for item in self.items.all())

class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product if self.product else self.mobile}"    