import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="w-screen bg-gray-100 shadow-md">
      <div className="max-w-5xl mx-auto px-6 py-4 flex justify-end">
        <ul className="flex space-x-8 text-gray-700 font-medium">
          <li>
            <Link to="/" className="hover:text-blue-600 transition-colors duration-200">
              Home
            </Link>
          </li>
          <li>
            <Link to="/login" className="hover:text-blue-600 transition-colors duration-200">
              Login
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;