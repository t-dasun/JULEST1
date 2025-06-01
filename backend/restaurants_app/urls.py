from django.urls import path, include # include is needed for nesting
from .views import (
    RestaurantListCreateView, MyRestaurantDetailView,
    MenuListCreateView, MenuDetailView,
    MenuItemListCreateView, MenuItemDetailView, MenuQRCodeView,
    PublicRestaurantDetailView,
    RestaurantOrderListView, RestaurantOrderDetailView, RestaurantOrderUpdateStatusView # New views
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

# Define owner order patterns
owner_order_patterns = [
    path('', RestaurantOrderListView.as_view(), name='owner-order-list'),
    path('<int:order_id>/', RestaurantOrderDetailView.as_view(), name='owner-order-detail'),
    path('<int:order_id>/status/', RestaurantOrderUpdateStatusView.as_view(), name='owner-order-update-status'),
]

urlpatterns = [
    # Path for:
    # GET /api/restaurants/ (Public list - handled by RestaurantListCreateView's GET)
    # POST /api/restaurants/ (Owner create - handled by RestaurantListCreateView's POST)
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),

    # Path for:
    # GET /api/restaurants/<id>/ (Public detail)
    path('<int:id>/', PublicRestaurantDetailView.as_view(), name='public-restaurant-detail'),

    # Owner specific paths
    path('my-restaurant/', MyRestaurantDetailView.as_view(), name='my-restaurant-detail'), # Manages the restaurant entity itself
    path('my-restaurant/menus/', include(menu_patterns)), # Manages menus for that restaurant
    path('my-restaurant/orders/', include(owner_order_patterns)), # New: Manages orders for that restaurant
]
