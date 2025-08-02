import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  return (
    <div className="max-w-md mx-auto mt-12 p-6">
      <h1>Register as a...</h1>
      <div className="max-w-md gap-4 flex mt-6 justify-center">
        <button onClick={() => navigate("/learner")}>Learner</button>
        <button onClick={() => navigate("/employer")}>Employer</button>
      </div>
    </div>
  );
}

export default Register;