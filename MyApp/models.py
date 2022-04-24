from django.db import models
from django.contrib.auth.forms import User
from django.conf import settings
from django.shortcuts import reverse






# Create your models here.
class Category(models.Model):
    cid=models.AutoField
    cname=models.CharField(max_length=30)
    def __str__(self):
        return self.cname

class Product(models.Model):
    id=models.AutoField
    cat = models.ForeignKey(Category, on_delete="CASCADE", default=None)
    name=models.CharField(max_length=20)
    description=models.TextField(default=None)
    price=models.IntegerField()
    img1=models.ImageField(upload_to='images',default=None)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



class Wishp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete= models.CASCADE)

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    wid=models.AutoField
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wish_items = models.ManyToManyField(Wishp)


    def __str__(self):
        return str(self.user.username)



class Orderproduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{ self.quantity} of {self.item.name}"

    def get_totali(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_totali()





class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(Orderproduct)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Checkout(models.Model):
    checkid = models.AutoField
    chname = models.CharField(max_length=30)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=50)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    comment=models.TextField()

    def __str__(self):
            return self.chname





class Cart(models.Model):
    cartid = models.AutoField
    cart_user = models.ForeignKey(User, on_delete='CASCADE', default=None)
    cart_product = models.ForeignKey(Product, on_delete='CASCADE', default=None)
    count = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cart_user)





class ContactForm(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    message=models.TextField()


def news(request):
    news=newsletter()
    news.email=request.POST.get('email')
    news.save()

class newsletter(models.Model):
    email=models.CharField(max_length=30)








