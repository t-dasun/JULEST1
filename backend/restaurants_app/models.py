from django.db import models
from users.models import User # Assuming users.models.User is the correct path

class Restaurant(models.Model):
    """
    Represents a restaurant in the system.
    Each restaurant is owned by a User.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants_owned')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    cuisine_type = models.CharField(max_length=100, blank=True)
    logo_url = models.URLField(blank=True)
    # Ideally JSON, using TextField as a fallback if JSONField has issues.
    operating_hours = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'restaurants_app'


class Menu(models.Model):
    """
    Represents a menu for a specific restaurant.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    class Meta:
        app_label = 'restaurants_app'


class MenuItem(models.Model):
    """
    Represents an individual item on a menu.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'restaurants_app'
