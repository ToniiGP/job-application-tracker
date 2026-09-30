import { useEffect, useState } from "react"

function Dashboard() {
  const [user, setUser] = useState(null)

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

    fetchUser()
  }, [])

  return (
    <div>
      <h1>Dashboard</h1>

      {user && (
        <p>Welcome, {user.username}!</p>
      )}
    </div>
  )
}

export default Dashboard