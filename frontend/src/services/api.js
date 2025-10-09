import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token endpoints
export const getNewTokens = async (page = 1, pageSize = 20, network = null, confirmedOnly = true) => {
  const params = { page, page_size: pageSize, confirmed_only: confirmedOnly };
  if (network) params.network = network;
  
  const response = await api.get('/tokens/new', { params });
  return response.data;
};

export const getTokenById = async (tokenId) => {
  const response = await api.get(`/tokens/${tokenId}`);
  return response.data;
};

export const getTokenByAddress = async (address, network) => {
  const response = await api.get(`/tokens/address/${address}`, { params: { network } });
  return response.data;
};

// Stats endpoints
export const getStats = async () => {
  const response = await api.get('/stats/summary');
  return response.data;
};

// Alerts endpoints
export const getRecentAlerts = async (limit = 10) => {
  const response = await api.get('/alerts/recent', { params: { limit } });
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;


