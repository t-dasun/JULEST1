import React from 'react';
import { Link } from 'react-router-dom';

const RestaurantCard = ({ restaurant }) => {
  return (
    <div style={{ border: '1px solid #ddd', padding: '1rem', margin: '1rem', width: '300px' }}>
      {restaurant.logo_url &&
        <img src={restaurant.logo_url} alt={restaurant.name} style={{ maxWidth: '100%', height: '150px', objectFit: 'cover' }} />}
      <h3>{restaurant.name}</h3>
      <p>Cuisine: {restaurant.cuisine_type}</p>
      <p>Address: {restaurant.address}</p>
      <Link to={`/restaurants/${restaurant.id}`}>View Menu</Link>
    </div>
  );
};
export default RestaurantCard;
