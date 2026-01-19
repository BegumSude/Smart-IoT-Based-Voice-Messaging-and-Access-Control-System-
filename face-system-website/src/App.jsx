import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './pages/login'
import MainLayout from './mainLayout'
function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<LoginPage />} />

        {/* Protected pages */}
        <Route
          path="/home"
          element={
      
              <MainLayout />
      
          }
        />
        <Route
          path="/admin"
          element={
      
                <MainLayout />
            
          }
        />

      </Routes>
    </BrowserRouter>
  )
}

export default App
