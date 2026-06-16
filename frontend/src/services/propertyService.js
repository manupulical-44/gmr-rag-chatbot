import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
});

export const propertyService = {
  async getProperties(params = {}) {
    const response = await api.get('/properties', { params });
    return response.data;
  },

  async getPropertyById(propertyId) {
    const response = await api.get(`/properties/${propertyId}`);
    return response.data;
  },

  async getFeaturedProperties(limit = 6) {
    const response = await api.get('/properties/featured', { params: { limit } });
    return response.data;
  },

  async getSimilarProperties(propertyId, limit = 4) {
    const response = await api.get(`/properties/${propertyId}/similar`, { params: { limit } });
    return response.data;
  },
};
