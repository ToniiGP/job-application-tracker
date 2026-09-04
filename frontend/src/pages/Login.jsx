import {useState} from "react"

function Login()
{
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    function handleSubmit(event){
        event.preventDefault()

        console.log("Email:", email)
        console.log("Password:", password)
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

                <button type="submit">
                    Login
                </button>
            </form>

        </div>
    )
}

export default Login 