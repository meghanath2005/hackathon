import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

export const getCyclones = async () => (await client.get('/cyclones')).data;
export const predictClassical = async (payload) => (await client.post('/predict/classical', payload)).data;
export const predictHybrid = async (payload) => (await client.post('/predict/hybrid', payload)).data;
export const getMetrics = async () => (await client.get('/metrics')).data;
