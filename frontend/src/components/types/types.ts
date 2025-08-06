export interface BaseUser {
  name: string;
  email: string;
  password: string;
  role: 'learner' | 'employer' | 'admin';
}

export interface Learner extends BaseUser {
  resume?: string;
  certifications?: string[]; 
  skills?: string[];
  learner_id?: number;
}

export interface Employer extends BaseUser {
  company_name: string;
  contact_info?: string;
}
