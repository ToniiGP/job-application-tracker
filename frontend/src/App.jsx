
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"
import CreateApplication from "./pages/CreateApplication"
import ApplicationDetails from "./pages/ApplicationDetails"

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/applications/new" element={<CreateApplication />}/>
        <Route path="/applications/:id" element={<ApplicationDetails />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App