import axios from 'axios'

const api_base_url = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: api_base_url,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login/', { username, password })
    return response.data
  },
  async logout() {
    await api.post('/auth/logout/')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}

export const crmService = {
  async getDashboardStats() {
    const response = await api.get('/dashboard/stats/')
    return response.data
  },
  async getCompanies() {
    const response = await api.get('/companies/')
    return response.data
  },
  async createCompany(data) {
    const response = await api.post('/companies/', data)
    return response.data
  },
  async getContacts() {
    const response = await api.get('/contacts/')
    return response.data
  },
  async createContact(data) {
    const response = await api.post('/contacts/', data)
    return response.data
  },
  async getDeals() {
    const response = await api.get('/deals/')
    return response.data
  },
  async createDeal(data) {
    const response = await api.post('/deals/', data)
    return response.data
  },
}

export default api
