import axios from 'axios';

const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api`;

export const checkHealth = async () => {
  const response = await axios.get(`${API_BASE_URL}/health`);
  return response.data;
};

export const predictTextNews = async (text) => {
  const response = await axios.post(`${API_BASE_URL}/predict/text`, { text });
  return response.data;
};

export const predictImageNews = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await axios.post(`${API_BASE_URL}/predict/image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const verifyNewsSources = async (text) => {
  const response = await axios.post(`${API_BASE_URL}/verify`, { text });
  return response.data;
};
