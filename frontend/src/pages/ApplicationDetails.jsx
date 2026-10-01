import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

function ApplicationDetails() {
  const { id } = useParams()

  const [application, setApplication] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchApplication() {
      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://localhost:8000/applications/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (response.ok) {
        setApplication(data)
        setError("")
      } else {
        setError(data.detail || "Could not load application")
      }
    }

    fetchApplication()
  }, [id])

  return (
    <div>
      <h1>Application Details</h1>

      {error && <p>{error}</p>}

      {application && (
        <div>
          <h2>{application.company_name}</h2>
          <p>Job Title: {application.job_title}</p>
          <p>Status: {application.status}</p>
          <p>Location: {application.location}</p>
          <p>Date Applied: {application.date_applied}</p>
          <p>Notes: {application.notes}</p>
        </div>
      )}
    </div>
  )
}

export default ApplicationDetails