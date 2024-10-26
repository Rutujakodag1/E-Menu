
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Category/')
    
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='food_items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='FoodItem/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Model to store food items that are not submitted
class NotSubmittedItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='NotSubmitted/')
    tableNumber=models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"Food Item: {self.food_item.name}, "
            f"Name: {self.name}, "
            f"Price: {self.price}, "
            f"Image: {self.image.url if self.image else 'No Image'}, "
            f"Table Number: {self.tableNumber}, "
            f"Quantity: {self.quantity}"
        )

# Model to store submitted food items for billing
class SubmittedItem(models.Model):
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Submitted/')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Allow blank and calculate in save()
    tableNumber = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, default='pending')  # Default to pending
    created_at = models.DateTimeField(auto_now_add=True)  # New field to track creation time

    def save(self, *args, **kwargs):
        # Automatically calculate total price on save
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Food Item: {self.food_item.name}, "
            f"Name: {self.name}, "
            f"Price: {self.price}, "
            f"Quantity: {self.quantity}, "
            f"Total Price: {self.total_price}, "
            f"Table Number: {self.tableNumber}, "
            f"Status: {self.status}"
            f"Created At: {self.created_at}"
        )

class orders(models.Model):
    tableNumber = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Name: {self.name}, "
            f"Quantity: {self.quantity}, "
            f"Price: {self.price}, "
            f"Total Price: {self.total_price}, "
            f"Table Number: {self.tableNumber}, "
            f"Status: {self.status}"
        )


