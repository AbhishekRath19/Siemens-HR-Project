import { useState } from 'react'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import axios from 'axios'

export default function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [files, setFiles] = useState([])
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) {
      setError('Please paste a job description first.')
      return
    }
    if (files.length === 0) {
      setError('Please upload at least one resume PDF.')
      return
    }
    setError(null)
    setLoading(true)
    setResults(null)

    const formData = new FormData()
    formData.append('job_description', jobDescription)
    files.forEach(f => formData.append('files', f))

    try {
      const res = await axios.post('http://localhost:8000/analyze', formData)
      setResults(res.data.results)
    } catch (err) {
      setError('Backend error. Make sure the API server is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-bg font-inter flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          files={files}
          setFiles={setFiles}
          onAnalyze={handleAnalyze}
          loading={loading}
          error={error}
        />
        <Dashboard results={results} loading={loading} />
      </div>
    </div>
  )
}