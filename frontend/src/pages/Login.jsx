import {useState} from "react"

function Login()
{
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    async function handleSubmit(event){
        event.preventDefault()

        const formData = new URLSearchParams()

        formData.append("username", email)
        formData.append("password", password)

        const response = await fetch("http://localhost:8000/auth/login", {
            method: "POST", 
            headers: {
                "Content-Type" : "application/x-www-form-urlencoded",
            }, 
            body: formData, 
        })

        const data = await response.json()

        if(response.ok){
            localStorage.setItem("token", data.access_token)
            setError("")
            console.log("Login successful")
        } else{
            setError("Invalid email or password")
        }
        
    }
    return(
        <div>
            <h1>
                Login
            </h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                    />
                </div>

                <div>
                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event)=> setPassword(event.target.value)}
                    />

                </div>

                {error && <p>{error}</p>}

                <button type="submit">
                    Login
                </button>
            </form>

        </div>
    )
}

export default Login 