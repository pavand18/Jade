import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './components/Dashboard'
import Data from './pages/Data'
import Data3 from './pages/Data3'
import Data4 from './pages/Data4'
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
import Dashboard3 from './components/Dashboard3'
import Dashboard4 from './components/Dashboard4'
import Reconstruct2 from './pages/Reconstruct2'
import Reconstruct3 from './pages/Reconstruct3'
import Reconstruct4 from './pages/Reconstruct4'
import Original2 from './pages/Original2'

// import LineChart from './pages/LineChart'
import Col1 from './components/Dcol'
import Compress from './pages/Compress3'
import Data2 from './pages/Data2'

function App() {
  return (
    <>
      <Router>
        <Topbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard2" element={<Dashboard2 />} />
          <Route path="/dashboard3" element={<Dashboard3 />} />
          <Route path="/dashboard4" element={<Dashboard4 />} />

          <Route path="/upload1" element={<Upload1 />} />
          <Route path="/upload2" element={<Upload2 />} />
          <Route path="/upload3" element={<Upload3 />} />
          <Route path="/upload4" element={<Upload4 />} />
          <Route path="/dashboard/data" element={<Data />} />
          <Route path="/dashboard2/data2" element={<Data2 />} />
          <Route path="/dashboard3/data3" element={<Data3 />} />
          <Route path="/dashboard4/data4" element={<Data4 />} />


          <Route path="/dashboard/standardise" element={<Standardise />} />
          <Route path="/dashboard3/compress3" element={<Compress />} />

          <Route path="/dashboard/submit" element={<NumberInputForm />} />
          <Route path="/dashboard/pca" element={<Pca />} />
          <Route path="/dashboard/reconstruct" element={<Reconstruct />} />
          <Route path="/dashboard2/reconstruct2" element={<Reconstruct2 />} />
          <Route path="/dashboard3/reconstruct3" element={<Reconstruct3 />} />
          <Route path="/dashboard4/reconstruct4" element={<Reconstruct4 />} />

          <Route path="/dashboard/col1" element={<Col1 /> } />
          <Route path="/dashboard/original" element={<Original />} />
          <Route path="/dashboard2/original2" element={<Original2 />} />
          {/* <Route path="/dashboard2/original2" element={<Original2 />} /> */}

        </Routes>
      </Router>
    </>
  )
}

export default App
