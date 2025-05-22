from django.urls import path, include # include is needed for nesting
from .views import (
    RestaurantListCreateView, MyRestaurantDetailView,
    MenuListCreateView, MenuDetailView,
    MenuItemListCreateView, MenuItemDetailView,
    MenuQRCodeView # Added MenuQRCodeView
)

# Define menu item patterns first
menu_item_patterns = [
    path('', MenuItemListCreateView.as_view(), name='menuitem-list-create'),
    path('<int:item_id>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
]

# Define menu patterns, including nested item patterns
menu_patterns = [
    path('', MenuListCreateView.as_view(), name='menu-list-create'),
    path('<int:menu_id>/', MenuDetailView.as_view(), name='menu-detail'),
    path('<int:menu_id>/qr-code/', MenuQRCodeView.as_view(), name='menu-qr-code'), # New path
    path('<int:menu_id>/items/', include(menu_item_patterns)), # Nest item patterns
]

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'), # For POST /api/restaurants/
    # URLs related to the owner's specific restaurant
    path('my-restaurant/', MyRestaurantDetailView.as_view(), name='my-restaurant-detail'), # GET, PUT for the restaurant itself
    path('my-restaurant/menus/', include(menu_patterns)), # All menu and menu item operations for "my-restaurant"
]
