
# Create your models here.
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category=models.CharField(max_length=255)
    class Meta:
        verbose_name_plural =("categories")
    def __str__(self):
        return str(self.category)
    
class Type(models.Model):
    type=models.CharField(max_length=255)
    def __str__(self):
        return str(self.type)
    
class Food(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    counter=models.IntegerField(default=4)
    type=models.ForeignKey(Type,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.FloatField()
    is_available=models.BooleanField(default=True)
    image = models.ImageField(upload_to='images')  

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    STATUS_OPTION=[
        ("Placed","Placed"),
        ("Cooking","Cooking"),
        ("Ready","Ready"),
        ("Delivered","Delivered"),
        ("Canceled","Canceled")
    ]

    PAYMENT_MODES=[
        ("ERP","ERP"),
        ("ONLINE","ONLINE")
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    counter=models.IntegerField()
    quantity=models.IntegerField()
    price=models.FloatField()
    status=models.CharField(max_length=20,choices=STATUS_OPTION,default='Placed')
    Payment_method=models.CharField(max_length=20,choices=PAYMENT_MODES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name+" "+self.food.name

class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    food=models.ForeignKey(Food,on_delete=models.DO_NOTHING)
    rating=models.IntegerField()
    comment=models.TextField()

    def __str__(self):
        return self.food.name+" - "+self.comment

