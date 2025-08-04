import axios from 'axios';
import type { BaseUser, Learner, Employer } from '../types/types';

const API_URL = 'https://your-api-url.com/api/register'; // TODO: Replace with actual API endpoint

export const registerUser = async (userData: BaseUser | Learner | Employer) => {
  try {
    const response = await axios.post(API_URL, userData);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response?.data?.message) {
      throw new Error(error.response.data.message);
    }
    throw new Error('Registration failed');
  }
};