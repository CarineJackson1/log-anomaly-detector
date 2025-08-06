import { Link } from "react-router-dom";
import './NavStyles.css'

function Navbar() {
  return (
    <nav className="navbar">
        <Link className="navbar-brand" to="/">
          AstroSkill
        </Link>
        <ul className="NavLink-Container">
          <li className="NavLinks">
            <Link className="nav-link" to="/#mission">
              Mission
            </Link>
          </li>
          <li className="NavLinks">
            <Link className="nav-link" to="/login">
              Login
            </Link>
          </li>
          <li className="NavLinks">
            <Link className="nav-link" to="/register">
              Register
            </Link>
          </li>
          <li className="NavLinks">
            <Link className="nav-link" to="/employer">
              Employer
            </Link>
          </li>
          <li className="NavLinks">
            <Link className="nav-link" to="/learner">
              Learner
            </Link>
          </li>
        </ul>
    </nav>
  );
}

export default Navbar;
