import { useEffect, useState } from "react"
import ApplicationCard from "../components/ApplicationCard"

function Dashboard() {
  const [user, setUser] = useState(null)
  const [applications, setApplications] = useState([])

  useEffect(() => {
    async function fetchUser() {
      const token = localStorage.getItem("token")

      const response = await fetch("http://localhost:8000/users/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      if (response.ok) {
        setUser(data)
      }
    }

    async function fetchApplications() {
      const token = localStorage.getItem("token")

      const response = await fetch("http://localhost:8000/applications/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      if (response.ok) {
        setApplications(data)
      }
    }

    fetchUser()
    fetchApplications()
  }, [])

  return (
    <div>
      <h1>Dashboard</h1>

      {user && <p>Welcome, {user.username}!</p>}

      <h2>Your Applications</h2>

      {applications.map((application) => (
        <ApplicationCard
          key={application.id}
          company={application.company_name}
          jobTitle={application.job_title}
          status={application.status}
        />
      ))}
    </div>
  )
}

export default Dashboard