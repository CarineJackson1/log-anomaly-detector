import axios from 'axios';
import type { BaseUser, Learner, Employer } from '../types/types';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const registerUser = async (data: BaseUser | Learner | Employer) => {
  try {
    const response = await axios.post(`${API_BASE}/auth/register`, data);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response?.data?.message) {
      throw new Error(error.response.data.message);
    }
    throw new Error('Registration failed');
  }
};