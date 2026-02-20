import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const fetchThreats = () => API.get('/threats');
export const fetchStats = () => API.get('/stats');