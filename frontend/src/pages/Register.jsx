import {useState} from "react"

function Register()
{
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    async function handleSubmit(event)
    {
        event.preventDefault()

        const response = await fetch("http://localhost:8000/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password,
            }),
        })

        const data = await response.json()

        if(response.ok)
            {
                setError("")
                console.log("account created successfuly")
            }else{
                setError(data.detail || "Something went wrong, please try again")
            }
    }
    return(
        <div> 
            <h1>
                Register
            </h1>

            <form onSubmit = {handleSubmit}>
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
                        Username
                    </label>

                    <input
                        type="text"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </div>

                <div>
                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                    />
                </div>

                {error && <p>{error}</p>}

                <button type="submit">
                    Register
                </button>
            </form>
        </div>
    )

}

export default Register