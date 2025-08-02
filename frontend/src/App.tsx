import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Learner from "./pages/Learner";
import Employer from "./pages/Employer";

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col w-screen">
        <Navbar />
        <main className="flex-grow w-full max-w-5xl mx-auto p-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/learner" element={<Learner />} />
            <Route path="/employer" element={<Employer />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
