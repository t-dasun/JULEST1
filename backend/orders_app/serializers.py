from rest_framework import serializers
from .models import Order, OrderItem
from restaurants_app.models import MenuItem, Restaurant # For validation and fetching details

# Serializer for creating individual order items (input only)
class OrderItemCreationSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_menu_item_id(self, value):
        """
        Check if the menu_item_id corresponds to an existing and available MenuItem.
        """
        try:
            menu_item = MenuItem.objects.get(id=value)
            if not menu_item.is_available:
                raise serializers.ValidationError(f"Menu item '{menu_item.name}' is not currently available.")
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("Menu item with this ID does not exist.")
        return value

# Serializer for displaying order item details
class OrderItemDetailSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    # menu_item_category = serializers.CharField(source='menu_item.category', read_only=True) # Example for more detail

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'menu_item', # This will show menu_item_id by default
            'menu_item_name',
            # 'menu_item_category',
            'quantity',
            'price_at_time_of_order'
        ]
        read_only_fields = ['price_at_time_of_order']

# Serializer for creating an order
class OrderCreationSerializer(serializers.ModelSerializer):
    items = OrderItemCreationSerializer(many=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source='restaurant', # This maps restaurant_id in payload to restaurant field in model
        write_only=True     # Only use for writing, not for representation
    )

    class Meta:
        model = Order
        fields = [
            'restaurant_id',
            'order_type',
            'delivery_address',
            'special_instructions',
            'items'
        ]
        # customer is set in the view
        # total_amount is calculated in the view
        # status is set to 'pending' by default in the model or view

    def validate_items(self, items_data):
        if not items_data:
            raise serializers.ValidationError("Order must contain at least one item.")

        # Further validation for each item can be done here if OrderItemCreationSerializer is not enough
        # For example, checking if all menu items belong to the specified restaurant_id
        restaurant = self.initial_data.get('restaurant_id')
        if restaurant: # restaurant_id might not be validated yet if it's invalid
            try:
                restaurant_obj = Restaurant.objects.get(id=restaurant)
                for item_data in items_data:
                    menu_item_id = item_data.get('menu_item_id')
                    try:
                        menu_item = MenuItem.objects.get(id=menu_item_id)
                        if menu_item.menu.restaurant != restaurant_obj:
                            raise serializers.ValidationError(
                                f"Menu item '{menu_item.name}' does not belong to the specified restaurant."
                            )
                    except MenuItem.DoesNotExist:
                        # This should already be caught by OrderItemCreationSerializer's validation
                        pass # Error handled by OrderItemCreationSerializer
            except Restaurant.DoesNotExist:
                 # This will be caught by PrimaryKeyRelatedField validation for restaurant_id
                pass
        return items_data

    def validate_delivery_address(self, value):
        order_type = self.initial_data.get('order_type')
        if order_type == Order.ORDER_TYPE_CHOICES[2][0]: # 'delivery'
            if not value or value.strip() == "":
                raise serializers.ValidationError("Delivery address is required for delivery orders.")
        elif value: # If address is provided for non-delivery orders
            # Optionally, clear it or raise a warning/error depending on desired behavior
            # For now, let's allow it but it might be ignored by the application logic
            pass
        return value

# Serializer for displaying full order details
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    # restaurant_logo_url = serializers.URLField(source='restaurant.logo_url', read_only=True) # Example

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'customer_username',
            'restaurant',
            'restaurant_name',
            # 'restaurant_logo_url',
            'order_type',
            'status',
            'total_amount',
            'delivery_address',
            'special_instructions',
            'items',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'customer',
            'restaurant',
            'status',
            'total_amount',
            'created_at',
            'updated_at'
        ]
