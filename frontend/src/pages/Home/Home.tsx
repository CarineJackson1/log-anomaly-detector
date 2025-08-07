// pages/Home/Home.tsx
import "./Home.css";
import { Mission } from './Mission';

export const Home = () => {
  // This function will handle the scroll action.
  const handleScrollToMission = () => {
    const missionSection = document.getElementById("mission");
    if (missionSection) {
      missionSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  // REMOVED: The useEffect that was here is gone, as it caused the scroll on page load.

  return (
    <>
      <div className="home-page-wrapper">
        <section className="hero">
          <div className="home-wrapper">
            <div className="home-left">
              <h1 className="homeh1">From Curiosity to Cosmos</h1>
              <h2 className="homeh2">
                Empowering Tomorrow's Aerospace Workforce
              </h2>
            </div>
            <div className="actBtn-wrapper">
              {/* MODIFIED: Added the onClick handler to the button */}
              <button className="act-btn" onClick={handleScrollToMission}>
                Start Your Journey
              </button>
            </div>
          </div>
        </section>

        <section id="mission">
          <Mission />
        </section>
      </div>
    </>
  );
};