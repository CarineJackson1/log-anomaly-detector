import React, { useState } from "react";
import type { Employer } from "../types/types";
import { useRegister } from "./useRegister";

const EmployerForm: React.FC = () => {
  const [formData, setFormData] = useState<
  Employer & { confirmPassword: string }
>({
  email: "",
  password: "",
  confirmPassword: "",
  name: "",            
  company_name: "", 
  role: "employer",
});

  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const { mutate: register, isPending, isSuccess, error } = useRegister();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validate = () => {
    const newErrors: { [key: string]: string } = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex =
      /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!emailRegex.test(formData.email)) {
      newErrors.email = "Invalid email address.";
    }

    if (!passwordRegex.test(formData.password)) {
      newErrors.password =
        "Password must be at least 8 characters, contain a letter, a number, and a special character.";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match.";
    }

    if (!formData.name) newErrors.firstName = "Name is required.";
    if (!formData.company_name)
      newErrors.companyName = "Company name is required.";

    return newErrors;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length === 0) {
      // Omit confirmPassword before submitting to API
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { confirmPassword, ...cleanedData } = formData;
      register(cleanedData);
    } else {
      setErrors(validationErrors);
    }
  };

  return (
    <div className="container">
      <div className="card shadow">
        <div className="card-body">
          <h4 className="card-title text-center mb-4">
            Explore top Aerospace talent!
          </h4>
          <form onSubmit={handleSubmit} noValidate>
            <div className="mb-3">
              <label>Name</label>
              <input
                type="text"
                name="firstName"
                className={`form-control ${
                  errors.name ? "is-invalid" : ""
                }`}
                value={formData.name}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.name}</div>
            </div>

            <div className="mb-3">
              <label>Email</label>
              <input
                type="email"
                name="email"
                className={`form-control ${errors.email ? "is-invalid" : ""}`}
                value={formData.email}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.email}</div>
            </div>

            <div className="mb-3">
              <label>Company Name</label>
              <input
                type="text"
                name="companyName"
                className={`form-control ${
                  errors.companyName ? "is-invalid" : ""
                }`}
                value={formData.company_name}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.companyName}</div>
            </div>


            <div className="mb-3">
              <label>Password</label>
              <input
                type="password"
                name="password"
                className={`form-control ${
                  errors.password ? "is-invalid" : ""
                }`}
                value={formData.password}
                onChange={handleChange}
              />
              <small className="form-text text-muted">
                Must be at least 8 characters, include a letter, number, and
                special character.
              </small>
              <div className="invalid-feedback">{errors.password}</div>
            </div>

            <div className="mb-3">
              <label>Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                className={`form-control ${
                  errors.confirmPassword ? "is-invalid" : ""
                }`}
                value={formData.confirmPassword}
                onChange={handleChange}
              />
              <div className="invalid-feedback">{errors.confirmPassword}</div>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isPending}
            >
              {isPending ? "Registering..." : "Register"}
            </button>

            {isSuccess && (
              <div className="alert alert-success mt-3">
                Successfully registered!
              </div>
            )}
            {error && (
              <div className="alert alert-danger mt-3">
                {(error as Error).message}
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default EmployerForm;
