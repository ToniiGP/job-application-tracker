import { Link } from "react-router-dom"

function ApplicationCard({ id, company, jobTitle, status }) {
  return (
    <div>
      <h3>{company}</h3>
      <p>{jobTitle}</p>
      <p>{status}</p>

      <Link to={`/applications/${id}`}>View Details</Link>
    </div>
  )
}

export default ApplicationCard