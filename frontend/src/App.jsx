import Navbar from "./components/NavBar"
import ApplicationCard from "./components/ApplicationCard"
import {useState} from "react"


function App() {

  const [showApplications, setShowApplications] = useState(true)

  return (
    <div>
      <Navbar />
      <h1>Job Application Tracker</h1>
      <p>Track your applications and interviews.</p>

      <button onClick={() => setShowApplications(!showApplications)}>
        Show/Hide Applications
      </button>

      {showApplications && (
        <div>
          <ApplicationCard
            company="Google"
            jobTitle="Software Engineer"
            status="Applied"
          />

          <ApplicationCard
            company="Microsoft"
            jobTitle="Backend Engineer"
            status="Technical Interview"
          />
        </div>
      )}

    </div>
  )
}

export default App
