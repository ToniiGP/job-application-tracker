import { useState } from "react"
import { useNavigate } from "react-router-dom"

function CreateApplication() {
  const navigate = useNavigate()
  const [companyName, setCompanyName] = useState("")
  const [jobTitle, setJobTitle] = useState("")
  const [status, setStatus] = useState("Wishlist")
  const [location, setLocation] = useState("")
  const [jobUrl, setJobUrl] = useState("")
  const [dateApplied, setDateApplied] = useState("")
  const [notes, setNotes] = useState("")
  const [error, setError] = useState("")

  async function handleSubmit(event) {
    event.preventDefault()

    const token = localStorage.getItem("token")

    const response = await fetch("http://localhost:8000/applications/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        company_name: companyName,
        job_title: jobTitle,
        status: status,
        location: location,
        job_url: jobUrl,
        date_applied: dateApplied || null,
        notes: notes,
      }),
    })

    const data = await response.json()

    if (response.ok) {
        console.log("SUCCESS - redirecting to dashboard")
        setError("")
        navigate("/dashboard")
    } else {
        console.log("ERROR:", data)
        setError(data.detail || "Something went wrong")
    }
  }

  return (
    <div>
      <h1>Add Application</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Company Name</label>
          <input
            type="text"
            value={companyName}
            onChange={(event) => setCompanyName(event.target.value)}
          />
        </div>

        <div>
          <label>Job Title</label>
          <input
            type="text"
            value={jobTitle}
            onChange={(event) => setJobTitle(event.target.value)}
          />
        </div>

        <div>
          <label>Status</label>
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          >
            <option value="Wishlist">Wishlist</option>
            <option value="Applied">Applied</option>
            <option value="Online Assessment">Online Assessment</option>
            <option value="Phone Screen">Phone Screen</option>
            <option value="Technical Interview">Technical Interview</option>
            <option value="Final Interview">Final Interview</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
            <option value="Withdrawn">Withdrawn</option>
          </select>
        </div>

        <div>
          <label>Location</label>
          <input
            type="text"
            value={location}
            onChange={(event) => setLocation(event.target.value)}
          />
        </div>

        <div>
          <label>Job URL</label>
          <input
            type="url"
            value={jobUrl}
            onChange={(event) => setJobUrl(event.target.value)}
          />
        </div>

        <div>
          <label>Date Applied</label>
          <input
            type="date"
            value={dateApplied}
            onChange={(event) => setDateApplied(event.target.value)}
          />
        </div>

        <div>
          <label>Notes</label>
          <textarea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
          />
        </div>

        {error && <p>{error}</p>}

        <button type="submit">Add Application</button>
      </form>
    </div>
  )
}

export default CreateApplication