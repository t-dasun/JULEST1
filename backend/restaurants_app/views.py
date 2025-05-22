from rest_framework import generics, permissions, views # Added views for APIView
from django.http import Http404, HttpResponse # Added HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer
from .models import Restaurant, Menu, MenuItem
from users.models import User
from .utils import generate_qr_code_to_bytes # Added QR code utility


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    Allows authenticated users (restaurant owners) to create a new restaurant.
    Listing all restaurants is also supported.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the owner of the restaurant to the currently authenticated user.
        """
        # Ensure the user has the 'owner' role before allowing creation
        if self.request.user.role != 'owner':
            # Using rest_framework.exceptions.PermissionDenied
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only users with the 'Restaurant Owner' role can create restaurants.")
        serializer.save(owner=self.request.user)

class MyRestaurantDetailView(generics.RetrieveUpdateAPIView):
    """
    Allows a restaurant owner to retrieve or update their own restaurant's details.
    This view assumes an owner might have one primary restaurant they manage via this endpoint,
    or if they have multiple, the URL should specify which one (not implemented here,
    this view implicitly handles one restaurant per owner for "my-restaurant" concept).
    """
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return restaurants owned by the current user.
        """
        # Ensure the user has the 'owner' role
        if self.request.user.role != 'owner':
            return Restaurant.objects.none() # Return an empty queryset if not an owner
        return Restaurant.objects.filter(owner=self.request.user)

    def get_object(self):
        """
        Retrieve the restaurant owned by the current user.
        Raises Http404 if the user does not own a restaurant or if multiple are found
        for a view that implies a single "my-restaurant".
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            raise Http404("No Restaurant found for the current user.")

        # If an owner can have multiple restaurants, this view should ideally take a 'pk'
        # from the URL to identify which restaurant. For a "my-restaurant" singular concept:
        if queryset.count() > 1:
            # This indicates an ambiguous situation for a "my-restaurant" singular view.
            # Depending on product decision, could return the first, or raise error.
            # For now, let's assume this view is for *the* restaurant if only one exists.
            # If multiple allowed, URL needs a pk.
            # Consider logging this situation if it's not expected.
            # For this task's simplicity, let's stick to the single-restaurant-per-owner assumption for this view
            # or require a more specific lookup if multiple can exist.
            # We will use get_object_or_404 which expects a single result from the queryset.
            # To make it work, the queryset needs to be further filtered by a pk from URL,
            # or we assume this view is for a user that is guaranteed to have only one restaurant.
            # Given the prompt's example `Restaurant.objects.get(owner=self.request.user)`,
            # it implies a single restaurant expectation for this specific view.
            pass

        # Using get_object_or_404 for robustness, ensure it gets a single object
        # If the queryset could return multiple, and no pk is in the URL,
        # .get() or get_object_or_404 without pk would fail if count > 1.
        # The prompt's example `Restaurant.objects.get(owner=self.request.user)` is good.
        try:
            # This is the most direct interpretation of the prompt's example for get_object
            obj = queryset.get() # This will raise MultipleObjectsReturned if more than one.
        except Restaurant.DoesNotExist: # Should be caught by queryset.exists() check above, but good for safety
            raise Http404("No Restaurant found for the current user.")
        except Restaurant.MultipleObjectsReturned:
            raise Http404("Multiple restaurants found for this user. This view requires a specific restaurant identifier.")

        self.check_object_permissions(self.request, obj) # Check object-level permissions
        return obj


# Menu Views
class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, owner=self.request.user)
        return Menu.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        if self.request.user.role != 'owner':
            raise PermissionDenied("Only users with the 'Restaurant Owner' role can create menus.")
        restaurant = get_object_or_404(Restaurant, owner=self.request.user)
        serializer.save(restaurant=restaurant)


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'menu_id'

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, owner=self.request.user)
        return Menu.objects.filter(restaurant=restaurant)

    def perform_update(self, serializer):
        if not self.request.user.role == 'owner':
            raise PermissionDenied("You do not have permission to perform this action.")
        # The queryset already ensures the menu belongs to the user's restaurant.
        # No need to explicitly set restaurant again unless it's being changed, which is not typical here.
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.role == 'owner':
            raise PermissionDenied("You do not have permission to perform this action.")
        instance.delete()


class MenuQRCodeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, id=menu_id, restaurant__owner=request.user)
        # Construct the frontend URL. This is a placeholder and might need adjustment
        # based on the actual frontend routing and domain.
        frontend_url = f"https://manu.lk/restaurants/{menu.restaurant.id}/menus/{menu.id}"
        
        qr_bytes = generate_qr_code_to_bytes(frontend_url)
        return HttpResponse(qr_bytes, content_type="image/png")


# MenuItem Views
class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure menu_id is for a menu owned by the user's restaurant
        menu = get_object_or_404(Menu, id=self.kwargs['menu_id'], restaurant__owner=self.request.user)
        return MenuItem.objects.filter(menu=menu)

    def perform_create(self, serializer):
        if self.request.user.role != 'owner':
            raise PermissionDenied("Only users with the 'Restaurant Owner' role can create menu items.")
        menu = get_object_or_404(Menu, id=self.kwargs['menu_id'], restaurant__owner=self.request.user)
        serializer.save(menu=menu)


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'item_id' # To match URL parameter for the item

    def get_queryset(self):
        # This queryset ensures that we only operate on items within a menu
        # that belongs to a restaurant owned by the requesting user.
        # The actual item is fetched by get_object using item_id from URL.
        menu = get_object_or_404(Menu, id=self.kwargs['menu_id'], restaurant__owner=self.request.user)
        return MenuItem.objects.filter(menu=menu)
        # Alternative: return MenuItem.objects.filter(menu_id=self.kwargs['menu_id'], menu__restaurant__owner=self.request.user)

    def get_object(self):
        # Use the queryset defined above to ensure user ownership context
        queryset = self.get_queryset()
        # Fetch the specific item using the item_id from the URL
        obj = get_object_or_404(queryset, id=self.kwargs['item_id'])
        self.check_object_permissions(self.request, obj) # Good practice
        return obj
        # Simpler alternative for get_object:
        # menu = get_object_or_404(Menu, id=self.kwargs['menu_id'], restaurant__owner=self.request.user)
        # menu_item = get_object_or_404(MenuItem, menu=menu, id=self.kwargs['item_id'])
        # return menu_item


    def perform_update(self, serializer):
        if not self.request.user.role == 'owner':
            raise PermissionDenied("You do not have permission to perform this action.")
        # Menu context is already validated by get_queryset/get_object
        # Ensure menu is passed if serializer requires it (e.g. if not read_only)
        # Since menu is read_only in serializer, it won't be part of validated_data.
        # If it were writable, we'd do:
        # menu = get_object_or_404(Menu, id=self.kwargs['menu_id'], restaurant__owner=self.request.user)
        # serializer.save(menu=menu)
        serializer.save()


    def perform_destroy(self, instance):
        if not self.request.user.role == 'owner':
            raise PermissionDenied("You do not have permission to perform this action.")
        instance.delete()
