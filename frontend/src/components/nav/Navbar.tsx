import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar navbar-light bg-light shadow-sm px-5">
      <div className="d-flex justify-content-between w-100 align-items-center">
        <Link className="navbar-brand fw-bold" to="/">
          AstroSkill
        </Link>
        <ul className="navbar-nav d-flex flex-row mb-0">
          <li className="nav-item mx-2">
            <Link className="nav-link" to="/#mission">
              Mission
            </Link>
          </li>
          <li className="nav-item mx-2">
            <Link className="nav-link" to="/login">
              Login
            </Link>
          </li>
          <li className="nav-item mx-2">
            <Link className="nav-link" to="/register">
              Register
            </Link>
          </li>
          <li className="nav-item mx-2">
            <Link className="nav-link" to="/employer">
              Employer
            </Link>
          </li>
          <li className="nav-item mx-2">
            <Link className="nav-link" to="/learner">
              Learner
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
