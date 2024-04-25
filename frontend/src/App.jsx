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
import NumberInputForm from './components/PcaInput'
import Upload1 from './pages/Upload1'
import Upload2 from './pages/Upload2'
import Upload3 from './pages/Upload3'
import Upload4 from './pages/Upload4'
import Dashboard2 from './components/Dashboard2'
import Reconstruct2 from './pages/Reconstruct2'
import Original2 from './pages/Original2'

// import LineChart from './pages/LineChart'
import Col1 from './components/Dcol'

function App() {
  return (
    <>
      <Router>
        <Topbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard2" element={<Dashboard2 />} />
          <Route path="/upload1" element={<Upload1 />} />
          <Route path="/upload2" element={<Upload2 />} />
          <Route path="/upload3" element={<Upload3 />} />
          <Route path="/upload4" element={<Upload4 />} />
          <Route path="/dashboard/data" element={<Data />} />
          <Route path="/dashboard/standardise" element={<Standardise />} />

          <Route path="/dashboard/submit" element={<NumberInputForm />} />
          <Route path="/dashboard/pca" element={<Pca />} />
          <Route path="/dashboard/reconstruct" element={<Reconstruct />} />
          <Route path="/dashboard2/reconstruct2" element={<Reconstruct2 />} />

          <Route path="/dashboard/col1" element={<Col1 /> } />
          <Route path="/dashboard/original" element={<Original />} />
          <Route path="/dashboard2/original2" element={<Original2 />} />

        </Routes>
      </Router>
    </>
  )
}

export default App
