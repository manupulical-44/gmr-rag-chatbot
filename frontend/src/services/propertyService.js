import axios from 'axios';
import { mockProperties } from '../data/mockProperties';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
});

export const propertyService = {
  async getProperties(params = {}) {
    try {
      const response = await api.get('/properties', { params });
      return response.data;
    } catch (error) {
      const query = String(params.query || '').trim().toLowerCase();
      const filtered = mockProperties.filter((property) => {
        const cityMatch = !params.city || property.city.toLowerCase().includes(params.city.toLowerCase());
        const stateMatch = !params.state || property.state.toLowerCase().includes(params.state.toLowerCase());
        const bhkMatch = !params.bhk || Number(property.bhk) === Number(params.bhk);
        const minPriceMatch = !params.minPrice || property.price >= Number(params.minPrice);
        const maxPriceMatch = !params.maxPrice || property.price <= Number(params.maxPrice);
        const queryMatch =
          !query ||
          [property.title, property.address, property.city, property.state, property.propertyType]
            .join(' ')
            .toLowerCase()
            .includes(query);

        return cityMatch && stateMatch && bhkMatch && minPriceMatch && maxPriceMatch && queryMatch;
      });

      return {
        data: filtered,
        pagination: {
          page: Number(params.page || 1),
          pageSize: Number(params.pageSize || 8),
          total: filtered.length,
          totalPages: Math.max(1, Math.ceil(filtered.length / Number(params.pageSize || 8)))
        }
      };
    }
  },

  async getPropertyById(propertyId) {
    try {
      const response = await api.get(`/properties/${propertyId}`);
      return response.data;
    } catch (error) {
      return mockProperties.find((property) => property.id === propertyId) || null;
    }
  },

  async getFeaturedProperties() {
    try {
      const response = await api.get('/properties/featured');
      return response.data;
    } catch (error) {
      return mockProperties.slice(0, 6);
    }
  },

  async getSimilarProperties(propertyId) {
    try {
      const response = await api.get(`/properties/${propertyId}/similar`);
      return response.data;
    } catch (error) {
      return mockProperties.filter((property) => property.id !== propertyId).slice(0, 4);
    }
  }
};