import { useState } from "react";
import { useNavigate } from "react-router-dom";

// This is the Learner login form that will display when the user selects "Learner" on the login page. 
// Once the user successfully logs in, they will be directed to the correct dashboard. 

// state variable initializing empty login form
const LearnerLogin: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  // state variables for statuses and errors 
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // function for updating the form with the data user enters
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    // Clear the error for this field on change
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: "" });
    }
  };
    
  // validation for a correct email and errors that will ensure fields are filled in 
  const validate = () => {
    const newErrors: { [key: string]: string } = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(formData.email)) {
      newErrors.email = "Invalid email address.";
    }

    if (!formData.password) {
      newErrors.password = "Password is required.";
    }

    return newErrors;
  };

  // function handling form submission 
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length === 0) {
      setIsLoggingIn(true);
      setError(null);
      setIsSuccess(false);

      try {
        // Simulate login request (replace with real login API)
        await new Promise((resolve) => setTimeout(resolve, 1000)); // Fake delay
        setIsSuccess(true);
        navigate("/learner"); // Navigate only after success
      } catch (err) {
        setError(err instanceof Error ? err.message : "Login failed. Please try again.");
      } finally {
        setIsLoggingIn(false);
      }
    } else {
      setErrors(validationErrors);
    }
  };

  return (
    <div className="container">
      <div className="card shadow">
        <div className="card-body">
          <h4 className="card-title text-center mb-4">Welcome Back!</h4>
          <form onSubmit={handleSubmit} noValidate>
            <div className="mb-3">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                name="email"
                className={`form-control ${errors.email ? "is-invalid" : ""}`}
                value={formData.email}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.email}</div>
            </div>

            <div className="mb-3">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                name="password"
                className={`form-control ${
                  errors.password ? "is-invalid" : ""
                }`}
                value={formData.password}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.password}</div>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isLoggingIn}
            >
              {isLoggingIn ? "Logging in..." : "Login"}
            </button>

            {isSuccess && (
              <div className="alert alert-success mt-3">
                Successfully logged in!
              </div>
            )}
            {error && (
              <div className="alert alert-danger mt-3">{error}</div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default LearnerLogin;
