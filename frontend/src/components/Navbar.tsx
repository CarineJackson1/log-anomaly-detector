import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="w-screen bg-gray-100 shadow-md">
      <div className="mx-10 px-3 py-4 flex justify-between items-center">
        <Link
          to="/"
          className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200"
        >
          AstroSkill
        </Link>

        <ul className="flex space-x-8 text-gray-700 font-medium">
          <Link
            to="/#mission"
            className="hover:text-blue-600 transition-colors duration-200"
          >
            Mission
          </Link>
          <li>
            <Link
              to="/login"
              className="hover:text-blue-600 transition-colors duration-200"
            >
              Login
            </Link>
          </li>
          <li>
            <Link
              to="/register"
              className="hover:text-blue-600 transition-colors duration-200"
            >
              Register
            </Link>
          </li>
          <li>
            <Link
              to="/Employer"
              className="hover:text-blue-600 transition-colors duration-200"
            >
              Employer
            </Link>
          </li>
          <li>
            <Link
              to="/Learner"
              className="hover:text-blue-600 transition-colors duration-200"
            >
              Learner
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
