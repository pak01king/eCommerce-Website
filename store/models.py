from django.db import models
from django.contrib.auth.models import User



class ColorOption(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='color_options/')
    color_code = models.CharField(max_length=7, blank=True, help_text='Cod hex ex: #000000')

    def __str__(self):
        return self.name

# Brand model

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    colors = models.ManyToManyField('ColorOption', blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    featured_in_hero = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    color = models.CharField(max_length=50, blank=True, help_text="Culoarea asociată acestei imagini, ex: negru, auriu etc.")

    def __str__(self):
        return f"Image for {self.product.title} ({self.color})"


# Adresă de livrare salvată pentru fiecare user

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shipping_address')
    full_name = models.CharField(max_length=120)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address = models.TextField()
    apartment = models.CharField(max_length=20, blank=True)
    house_number = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.full_name} ({self.user.username})'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)  # se va actualiza după PayPal

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'

    def total_price(self):
        return self.product.price * self.quantity




    