from rest_framework import serializers
from .models import Restaurant, Menu, MenuItem # Added Menu and MenuItem
# from users.serializers import UserDetailSerializer # Option for deeper owner details

class RestaurantSerializer(serializers.ModelSerializer):
    # If you want to show nested user details for the owner:
    # owner = UserDetailSerializer(read_only=True)
    # Or, if you want to allow setting owner by ID during creation (though typically set by request user):
    # owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    active_menus = serializers.SerializerMethodField() # Added for active menus

    class Meta:
        model = Restaurant
        fields = [
            'id',
            # 'owner', # For public browsing, owner details might not be needed or simplified. Keeping it for now.
            'name',
            'address',
            'phone_number',
            'description',
            'cuisine_type',
            'logo_url',
            'operating_hours',
            'active_menus', # Added field
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['owner'] # Owner is typically set based on the authenticated user.

    def get_active_menus(self, obj):
        # obj is the Restaurant instance
        # 'menus' is the related_name from Restaurant.menus
        active_menus_queryset = obj.menus.filter(is_active=True)
        return MenuSerializer(active_menus_queryset, many=True, context=self.context).data


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'image_url',
            'is_available',
            'menu', # menu_id will be used for writes if menu is not read_only
            'created_at',
            'updated_at',
        ]
        # 'menu' is typically set via URL context in view, or if writable, should not be read_only.
        # For creating items within a menu, the menu_id is usually part of the URL.
        # If menu is part of payload for creation, it should be writable.
        # Assuming 'menu' is part of the payload for now or set in view.
        # For this iteration, let's make it writable by default via its field on the model.
        # If it should be read_only (e.g. when listing items for a menu), adjust as needed.
        # The prompt suggests read_only_fields = ['menu'], which is fine if menu is always set by URL.
        read_only_fields = ['menu']


    def validate_price(self, value):
        """
        Check that the price is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value


class MenuSerializer(serializers.ModelSerializer):
    # items = MenuItemSerializer(many=True, read_only=True) # Replaced by available_items
    available_items = serializers.SerializerMethodField() # Added for available items

    class Meta:
        model = Menu
        fields = [
            'id',
            # 'restaurant', # For public browsing, restaurant ID might be implicit. Keeping it for now.
            'name',
            'description',
            'is_active',
            'available_items', # Replaced 'items'
            'created_at',
            'updated_at',
        ]
        # 'restaurant' is a ForeignKey, so it's represented by its ID by default, which is fine.
        # If we wanted to remove it from public view, we'd remove it from fields.
        # For now, keeping it as it links back to the Restaurant.
        read_only_fields = ['restaurant'] # Restaurant is typically set based on context

    def get_available_items(self, obj):
        # obj is the Menu instance
        available_items_queryset = obj.items.filter(is_available=True) # 'items' is the related_name from Menu.items
        return MenuItemSerializer(available_items_queryset, many=True, context=self.context).data
