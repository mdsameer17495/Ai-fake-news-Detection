import axios from 'axios';

const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api`;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export const checkHealth = async () => {
  const response = await apiClient.get('/health', { timeout: 15000 });
  return response.data;
};

export const predictTextNews = async (text) => {
  const response = await apiClient.post('/predict/text', { text });
  return response.data;
};

export const predictImageNews = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await apiClient.post('/predict/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const verifyNewsSources = async (text) => {
  const response = await apiClient.post('/verify', { text });
  return response.data;
};
