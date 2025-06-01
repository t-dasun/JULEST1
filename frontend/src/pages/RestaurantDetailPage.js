import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../services/api'; // Adjust path

const RestaurantDetailPage = () => {
  const { restaurantId } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRestaurantDetail = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get(`/restaurants/${restaurantId}/`);
        setRestaurant(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch restaurant details.');
        setLoading(false);
        console.error(err);
      }
    };
    fetchRestaurantDetail();
  }, [restaurantId]);

  if (loading) return <p>Loading restaurant details...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!restaurant) return <p>Restaurant not found.</p>;

  return (
    <div>
      <h2>{restaurant.name}</h2>
      <p><strong>Cuisine:</strong> {restaurant.cuisine_type}</p>
      <p><strong>Address:</strong> {restaurant.address}</p>
      <p><strong>Phone:</strong> {restaurant.phone_number}</p>
      <p><strong>Hours:</strong> {typeof restaurant.operating_hours === 'object' ? JSON.stringify(restaurant.operating_hours) : restaurant.operating_hours}</p>
      <p>{restaurant.description}</p>

      <h3>Menus</h3>
      {restaurant.active_menus && restaurant.active_menus.length > 0 ? (
        restaurant.active_menus.map(menu => (
          <div key={menu.id} style={{ marginLeft: '20px', marginBottom: '20px', border: '1px solid #eee', padding: '10px' }}>
            <h4>{menu.name}</h4>
            <p>{menu.description}</p>
            <h5>Items:</h5>
            {menu.available_items && menu.available_items.length > 0 ? (
              <ul style={{ listStyleType: 'none', paddingLeft: '0'}}>
                {menu.available_items.map(item => (
                  <li key={item.id} style={{ borderBottom: '1px solid #f0f0f0', padding: '5px 0' }}>
                    <strong>{item.name}</strong> - ${item.price}
                    <p style={{ fontSize: '0.9em', color: '#555' }}>{item.description}</p>
                    {/* Add to cart button will go here later */}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No available items in this menu.</p>
            )}
          </div>
        ))
      ) : (
        <p>No active menus available.</p>
      )}
    </div>
  );
};
export default RestaurantDetailPage;
