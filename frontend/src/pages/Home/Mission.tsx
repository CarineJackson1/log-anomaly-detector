import { useState } from 'react';
import './Home.css';
import './Mission2.css'

// --- Data for the new tabbed mission section ---
const missionTabs = [
  {
    id: 'learners',
    title: 'For Learners',
    text: 'Dive into a universe of opportunity. AstroSkill provides a direct launchpad to your career in aerospace. Access specialized courses, connect with mentors, and find internships or your first job with the industry’s leading companies. Your journey to the cosmos starts here.',
    image: '/images/learner-mission.jpg', // Example image path
  },
  {
    id: 'employers',
    title: 'For Employers',
    text: 'Discover the next generation of aerospace talent. Our platform is engineered to connect you with skilled, passionate, and pre-vetted candidates ready to contribute to your mission. Streamline your recruitment process and find the perfect fit for your team, from interns to experienced professionals.',
    image: '/images/employer-mission.jpg', // Example image path
  },
  {
    id: 'educators',
    title: 'For Educators',
    text: "Empower your students with a direct link to the aerospace industry. AstroSkill partners with educational institutions to provide a clear pathway for students, offering real-world projects, curriculum support, and valuable industry connections to prepare them for successful careers.",
    image: '/images/educator-mission.jpg', // Example image path
  },
];


export const Mission = () => {
  // State to toggle between the two mission page versions
  const [showV2, setShowV2] = useState(false);
  
  // State to manage the active tab in Version 2
  const [activeTab, setActiveTab] = useState(missionTabs[0].id);

  const activeTabData = missionTabs.find(tab => tab.id === activeTab);

  // --- Common Action Button Component ---
  const ActionButton = () => (
     <a href="/register" className="group cta flex py-3 px-12 no-underline font-poppins text-4xl text-white bg-[#6225E6] transition-all duration-1000 shadow-[6px_6px_0_black] -skew-x-15 hover:shadow-[10px_10px_0_#FBC638] hover:duration-500 focus:outline-none">
        <span className="skew-x-15 text-white">Get Started!</span>
        <span className="skew-x-15 w-[66px] h-[43px] ml-5 relative top-1 transition-all duration-500 group-hover:mr-[45px]">
          <svg width="66px" height="43px" viewBox="0 0 66 43" version="1.1" xmlns="http://www.w3.org/2000/svg">
            <g id="arrow" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
              <path className="one" d="M40.1543933,3.89485454 L43.9763149,0.139296592 C44.1708311,-0.0518420739 44.4826329,-0.0518571125 44.6771675,0.139262789 L65.6916134,20.7848311 C66.0855801,21.1718824 66.0911863,21.8050225 65.704135,22.1989893 C65.7000188,22.2031791 65.6958657,22.2073326 65.6916762,22.2114492 L44.677098,42.8607841 C44.4825957,43.0519059 44.1708242,43.0519358 43.9762853,42.8608513 L40.1545186,39.1069479 C39.9575152,38.9134427 39.9546793,38.5968729 40.1481845,38.3998695 C40.1502893,38.3977268 40.1524132,38.395603 40.1545562,38.3934985 L56.9937789,21.8567812 C57.1908028,21.6632968 57.193672,21.3467273 57.0001876,21.1497035 C56.9980647,21.1475418 56.9959223,21.1453995 56.9937605,21.1432767 L40.1545208,4.60825197 C39.9574869,4.41477773 39.9546013,4.09820839 40.1480756,3.90117456 C40.1501626,3.89904911 40.1522686,3.89694235 40.1543933,3.89485454 Z" fill="#FFFFFF"></path>
              <path className="two" d="M20.1543933,3.89485454 L23.9763149,0.139296592 C24.1708311,-0.0518420739 24.4826329,-0.0518571125 24.6771675,0.139262789 L45.6916134,20.7848311 C46.0855801,21.1718824 46.0911863,21.8050225 45.704135,22.1989893 C45.7000188,22.2031791 45.6958657,22.2073326 45.6916762,22.2114492 L24.677098,42.8607841 C24.4825957,43.0519059 24.1708242,43.0519358 23.9762853,42.8608513 L20.1545186,39.1069479 C19.9575152,38.9134427 19.9546793,38.5968729 20.1481845,38.3998695 C20.1502893,38.3977268 20.1524132,38.395603 20.1545562,38.3934985 L36.9937789,21.8567812 C37.1908028,21.6632968 37.193672,21.3467273 37.0001876,21.1497035 C36.9980647,21.1475418 36.9959223,21.1453995 36.9937605,21.1432767 L20.1545208,4.60825197 C19.9574869,4.41477773 19.9546013,4.09820839 20.1480756,3.90117456 C20.1501626,3.89904911 20.1522686,3.89694235 20.1543933,3.89485454 Z" fill="#FFFFFF"></path>
              <path className="three" d="M0.154393339,3.89485454 L3.97631488,0.139296592 C4.17083111,-0.0518420739 4.48263286,-0.0518571125 4.67716753,0.139262789 L25.6916134,20.7848311 C26.0855801,21.1718824 26.0911863,21.8050225 25.704135,22.1989893 C25.7000188,22.2031791 25.6958657,22.2073326 25.6916762,22.2114492 L4.67709797,42.8607841 C4.48259567,43.0519059 4.17082418,43.0519358 3.97628526,42.8608513 L0.154518591,39.1069479 C-0.0424848215,38.9134427 -0.0453206733,38.5968729 0.148184538,38.3998695 C0.150289256,38.3977268 0.152413239,38.395603 0.154556228,38.3934985 L16.9937789,21.8567812 C17.1908028,21.6632968 17.193672,21.3467273 17.0001876,21.1497035 C16.9980647,21.1475418 16.9959223,21.1453995 16.9937605,21.1432767 L0.15452076,4.60825197 C-0.0425130651,4.41477773 -0.0453986756,4.09820839 0.148075568,3.90117456 C0.150162624,3.89904911 0.152268631,3.89694235 0.154393339,3.89485454 Z" fill="#FFFFFF"></path>
            </g>
          </svg>
        </span>
    </a>
  );

  return (
    <section id="mission" className="mission">
      <div className="mission-toggle-wrapper">
          <button onClick={() => setShowV2(!showV2)} className="toggle-button">
             Switch to Version {showV2 ? '1' : '2'}
          </button>
      </div>
      
      {/* Conditional Rendering based on state */}
      {!showV2 ? (
        // --- MISSION VERSION 1 ---
        <>
          <h1 className="mission-title">Our Mission</h1>
          <div className="mission-content">
            <div className="mission-image-container">
              <img
                src="/images/mission-image.jpg"
                alt="A rocket launching, symbolizing our mission"
                className="mission-img-new"
              />
            </div>
            <div className="mission-right-column">
              <div className="mission-text-content">
                <h3 className="mission-subtitle">Connecting Ambition with Opportunity</h3>
                <p className="mission-description-new">
                  AstroSkill is dedicated to bridging the gap between aspiring aerospace professionals and the industry's leading companies. Our platform provides the tools, resources, and connections needed to launch a successful career.
                </p>
                <ul className="mission-highlights">
                  <li>Connect directly with top aerospace employers.</li>
                  <li>Access specialized, industry-relevant courses.</li>
                  <li>Build a standout professional portfolio to showcase your skills.</li>
                </ul>
              </div>
              <div className="missionbtn-wrapper">
                  <ActionButton />
              </div>
            </div>
          </div>
        </>
      ) : (
        // --- MISSION VERSION 2 (NEW TABBED LAYOUT) ---
        <div className="mission-v2-container">
            <h1 className="mission-title">Mission (Option 2)</h1>
            <nav className="mission-v2-navbar">
              {missionTabs.map(tab => (
                <button 
                  key={tab.id} 
                  className={`mission-v2-nav-item ${activeTab === tab.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.title}
                </button>
              ))}
            </nav>
            <div className="mission-v2-content">
                {activeTabData && (
                  <>
                    <div className="mission-v2-text">
                        <p>{activeTabData.text}</p>
                        <div className="missionbtn-wrapper">
                           <ActionButton />
                        </div>
                    </div>
                    <div className="mission-v2-image-container">
                        <img src={activeTabData.image} alt={activeTabData.title} className="mission-v2-image"/>
                    </div>
                  </>
                )}
            </div>
        </div>
      )}
    </section>
  );
};