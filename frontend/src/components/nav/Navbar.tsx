// components/nav/Navbar.tsx
import { Link } from "react-router-dom";
import './NavStyles.css'

function Navbar() {
  // This function will handle the click on the "Mission" link.
  const handleMissionClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault(); // Prevent the link from changing the URL hash.
    const missionSection = document.getElementById("mission");
    if (missionSection) {
      missionSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="navbar">
      <Link className="navbar-brand" to="/">
        AstroSkill
      </Link>
      <ul className="NavLink-Container">
        <li className="NavLinks">
          <Link className="nav-link" to="/">
            Home
          </Link>
        </li>
        <li className="NavLinks">
          <a className="nav-link" href="/#mission" onClick={handleMissionClick}>
            Mission
          </a>
        </li>
        {/* The rest of your links remain the same */}
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