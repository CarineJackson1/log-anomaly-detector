import { useMutation } from '@tanstack/react-query';
import { registerUser } from './register';
import type { BaseUser } from '../types/types';

export const useRegister = () => {
  return useMutation({
    mutationFn: (userData: BaseUser) => registerUser(userData),
  });
};