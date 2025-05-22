from django.db import models
from users.models import User
from restaurants_app.models import Restaurant, MenuItem

class Order(models.Model):
    """
    Represents an order placed by a customer for items from a restaurant.
    """
    ORDER_TYPE_CHOICES = [
        ('dine-in', 'Dine-in'),
        ('takeaway', 'Takeaway'),
        ('delivery', 'Delivery')
    ]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders_placed')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders_received') # Changed related_name to avoid clash
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.restaurant.name}"

    class Meta:
        app_label = 'orders_app'


class OrderItem(models.Model):
    """
    Represents an individual item within an order (line item).
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name if self.menu_item else 'N/A'}"

    class Meta:
        app_label = 'orders_app'


class Payment(models.Model):
    """
    Represents a payment associated with an order.
    """
    PAYMENT_METHOD_CHOICES = [
        ('card_online', 'Card Online'),
        ('cash', 'Cash')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

    class Meta:
        app_label = 'orders_app'
