import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // Assuming proxy is set up in package.json or backend is on same domain/port
                   // Or use full URL: 'http://localhost:8000/api' if backend is on 8000
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default apiClient;
