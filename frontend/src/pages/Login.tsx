import { useState } from 'react';
import LearnerLogin from '../components/Login-Forms/LearnerLogin';
import EmployerLogin from '../components/Login-Forms/EmployerLogin';


// This is the login page that will render the correct Login form corresponding to the button the user selects. 

function Login() {
  const [userType, setUserType] = useState<'learner' | 'employer' | null>(null);

  return (
    <div className="d-flex justify-content-center align-items-center">
      <div>
        <h2 className="my-4 text-center">Login</h2>

        
        <div className="mb-3 d-flex justify-content-center">
          <button
            className={`btn me-2 ${userType === 'learner' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setUserType('learner')}
          >
            Learner
          </button>
          <button
            className={`btn ${userType === 'employer' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setUserType('employer')}
          >
            Employer
          </button>
        </div>

        <div className="mt-4">
          {userType === 'learner' && <LearnerLogin />}
          {userType === 'employer' && <EmployerLogin />}
        </div>
       
        <h2 className="text-lg text-gray-600 text-center">
          Or sign up here!{" "}
          <a href="/register" className="text-blue-600 hover:underline">
            Register
          </a>
        </h2>

        
      </div>
    </div>
  );
}

export default Login;
