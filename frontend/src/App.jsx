import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './components/Dashboard'
import Data from './pages/Data'
import Standardise from './pages/Standardise'
import Pca from './pages/Pca'
import Reconstruct from './pages/Reconstruct'
import Original from './pages/Original'
import Topbar from './components/Topbar'
import NumberInputForm from './components/NumberInputForm'
import LineChart from './pages/LineChart'
import Col1 from './components/Col1'

function App() {
  return (
    <>
      <Router>
        <Topbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/data" element={<Data />} />
          <Route path="/dashboard/standardise" element={<Standardise />} />
          <Route path="/dashboard/submit" element={<NumberInputForm />} />
          <Route path="/dashboard/pca" element={<Pca />} />
          <Route path="/dashboard/reconstruct" element={<Reconstruct />} />
          <Route path="/dashboard/col1" element={<Col1 /> } />
          
          <Route path="/dashboard/original" element={<Original />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
