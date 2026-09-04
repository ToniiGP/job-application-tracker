function ApplicationCard({company, jobTitle, status}){
    return (
    <div>
      <h3>{company}</h3>
      <p>{jobTitle}</p>
      <p>{status}</p>
    </div>
    )
}

export default ApplicationCard