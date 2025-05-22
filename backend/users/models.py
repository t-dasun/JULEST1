from django.db import models

class User(models.Model):
    """
    Represents a user of the application.
    This can be a customer, a restaurant owner, or an administrator.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Restaurant Owner'),
        ('admin', 'Admin')
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django handles hashing
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'users'
