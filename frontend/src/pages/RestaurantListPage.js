import React, { useState, useEffect } from 'react';
import apiClient from '../services/api'; // Adjust path
import RestaurantCard from '../components/RestaurantCard'; // Adjust path

const RestaurantListPage = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/restaurants/');
        setRestaurants(response.data.results); // Assuming pagination, .results holds the data
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch restaurants.');
        setLoading(false);
        console.error(err);
      }
    };
    fetchRestaurants();
  }, []);

  if (loading) return <p>Loading restaurants...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Restaurants</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {restaurants.length > 0 ? (
          restaurants.map(restaurant => (
            <RestaurantCard key={restaurant.id} restaurant={restaurant} />
          ))
        ) : (
          <p>No restaurants found.</p>
        )}
      </div>
    </div>
  );
};
export default RestaurantListPage;
