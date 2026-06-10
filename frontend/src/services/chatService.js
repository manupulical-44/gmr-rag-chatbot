import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
});

export const chatService = {
  async sendMessage(message, history = []) {
    const response = await api.post('/chat', { message, history });
    return response.data;
  }
};