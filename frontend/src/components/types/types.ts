export interface BaseUser {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  userType: 'learner' | 'employer';
}

export interface Learner extends BaseUser {
  phoneNumber?: string;
  
}

export interface Employer extends BaseUser {
  companyName: string;
  jobTitle: string;
}