from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name'])<1:
            errors['first_name']="Please enter your first name!"
        if len(data['last_name'])<2:
            errors["last_name"]="Please enter at least 2 characters for your last name!"
        if len(data['email'])<1:
            errors["email"]="Please enter an email!"
        elif not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email address!"
        if len(data['password'])<8:
            errors['password']="Please enter at least 8 characters for your password!"
        if data['pw_confirm']!= data["password"]:
            errors['pw_confirm']="Please match your password to its confirmation!"
        return errors

class AddressManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        if len(data['address'])<1:
            errors['address']="Please enter an address"
        if len(data['city'])<1:
            errors['city']="Please enter a city"
        if len(data['state'])<1:
            errors['state']="Please enter a state"
        if len(data['zip_code'])<1:
            errors['zip_code']="Please enter a zip code"
        return errors

# class PaymentManager(models.Manager):
#     def basic_validator(self, data):
#         errors={}
#         if len(data['card'])<16:
#             errors['card']="Please enter an 16 digit credit card"
#         if len(data['code'])<3:
#             errors['code']="Please enter 3 digit security code"
#         if len(data['expiration'])="":
#             errors['expiration']="Please enter an expiration date"
#         return errors

# class ItemManager(models.Manager):
#     def basic_validator(self, data):
#         errors={}
#         if len(data['name'])<3:
#             errors['name']="Please a name of at least 3 characters"
#         if len(data['description'])<5:
#             errors['code']="Please enter a description of at least 5 characters."
#         if len(data['price'])="":
#             errors['price']="Please enter a price"
#         return errors




class User(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    address=models.ForeignKey(Address, related_name="users")
    billing_address.ForeignKey(Address, related_name="users")
    objects=UserManager()

class Address(models.Model):
    address=models.CharField(max_length=200)
    address_2=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=2)
    zip_code=models.IntegerField(max_length=5)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # user=models.ForeignKey(User, related_name="address")
    objects=AddressManager()

# class BillingAddress(models.Model):
#     address=models.CharField(max_length=200)
#     address_2=models.CharField(max_length=200)
#     city=models.CharField(max_length=200)
#     state=models.CharField(max_length=2)
#     zip_code=models.IntegerField(max_length=5)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     user=models.ForeignKey(User, related_name="address")
#     objects=AddressManager()


class Payment(models.Model):
    card=models.IntegerField(max_length=16)
    code=models.IntegerField(max_length=4)
    expiration=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="payments")
    objects=PaymentManager()

class Order (models.Model):
    amount=models.DecimalField(max_digits=6, decimal_places=2)
    status=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="orders")
    address=models.ForeignKey(Address, related_name="orders")
    billing_address=models.ForeignKey(Address, related_name="orders")

class OrderDetails(models.Model):
    quantity=models.IntegerField()
    order_id=models.ForeignKey(Order, related_name="order_details")
    item_id=models.ForeignKey(Item, related_name="order_details")

class Item(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=6, decimal_places=2)
    image=models.CharField(max_length=100)
    inventory=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    sizes=models.ForeignKey(Size, related_name="items")
    categories=models.ForeignKey(Category, related_name="items")
    gender=models.ForeignKey(Gender, related_name="genders")
    objects=ItemManager()

class Gender(models.Model):
    gender=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # items=models.ForeignKey(User, related_name="gender")

class Category(models.Model):
    category=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    gender=models.ForeignKey(Gender, related_name="categories")

class Size(models.Model):
    size=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)