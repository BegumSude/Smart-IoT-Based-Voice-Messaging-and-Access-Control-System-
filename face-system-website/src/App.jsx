import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './pages/login'
import MainLayout from './mainLayout'

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<LoginPage />} />

        {/* Protected pages */}
        <Route path="/" element={<MainLayout />}>
          {/* <Route path="/" element={<Dashboard />} /> */}
        </Route>

      </Routes>
    </BrowserRouter>
  )
}

export default App
