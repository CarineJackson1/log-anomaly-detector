import { Routes, Route } from "react-router-dom";
import Navbar from "./components/nav/Navbar";
import { Home } from "./pages/Home/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Learner from "./pages/Learner";
import Employer from "./pages/Employer";
import NotFound from "./pages/NotFound";
import "./App.css";

function App() {
  return (
    <>
      <div className="App-Container">
      <Navbar />
        <main className="flex-grow w-full mx-auto">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/learner" element={<Learner />} />
            <Route path="/employer" element={<Employer />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </>
  );
}

export default App;
