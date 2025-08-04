import { useState } from 'react';
import LearnerForm from '../components/Registration/LearnerForm';
import EmployerForm from '../components/Registration/EmployerForm';

export default function Register() {
  const [userType, setUserType] = useState<'learner' | 'employer' | null>(null);

  return (
    <div
      className="d-flex justify-content-center align-items-center"
    >
      <div>
        <h2 className="my-4 text-center">Register</h2>

        <div className="mb-3 d-flex justify-content-center">
          <button
            className={`btn me-2 ${userType === 'learner' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setUserType('learner')}
          >
            Register as Learner
          </button>
          <button
            className={`btn ${userType === 'employer' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setUserType('employer')}
          >
            Register as Employer
          </button>
        </div>

        {userType && (
          <p className="text-muted text-center">
            You are registering as a <strong>{userType === 'learner' ? 'Learner' : 'Employer'}</strong>.
          </p>
        )}

        {userType === 'learner' && <LearnerForm />}
        {userType === 'employer' && <EmployerForm />}
      </div>
    </div>
  );
}