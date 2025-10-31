import { useState, FormEvent } from 'react'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [lineWidth, setLineWidth] = useState<number>(1)
  const [lineSpace, setLineSpace] = useState<number>(20)
  const [previewUrl, setPreviewUrl] = useState<string>('')
  const [resultUrl, setResultUrl] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (!file.type.startsWith('image/png')) {
        setError('Please select a PNG image')
        return
      }
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setError('')
      setResultUrl('')
    }
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    
    if (!selectedFile) {
      setError('Please select an image')
      return
    }

    setLoading(true)
    setError('')

    const formData = new FormData()
    formData.append('image', selectedFile)
    formData.append('lineWidth', lineWidth.toString())
    formData.append('lineSpace', lineSpace.toString())

    try {
      const response = await fetch('/api/grid', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to process image')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      setResultUrl(url)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (resultUrl) {
      const a = document.createElement('a')
      a.href = resultUrl
      a.download = `grid-${selectedFile?.name || 'image.png'}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  }

  return (
    <div className="container">
      <h1>Grid Image Generator</h1>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="file-input">Upload PNG Image</label>
          <input
            id="file-input"
            type="file"
            accept="image/png"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="line-width">
            Line Width: {lineWidth}px
          </label>
          <input
            id="line-width"
            type="range"
            min="1"
            max="10"
            value={lineWidth}
            onChange={(e) => setLineWidth(Number(e.target.value))}
            className="slider"
          />
        </div>

        <div className="form-group">
          <label htmlFor="line-space">
            Line Space: {lineSpace}px
          </label>
          <input
            id="line-space"
            type="range"
            min="5"
            max="100"
            value={lineSpace}
            onChange={(e) => setLineSpace(Number(e.target.value))}
            className="slider"
          />
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={!selectedFile || loading} className="btn-primary">
          {loading ? 'Processing...' : 'Generate Grid'}
        </button>
      </form>

      <div className="preview-container">
        {previewUrl && (
          <div className="preview">
            <h3>Original Image</h3>
            <img src={previewUrl} alt="Original" />
          </div>
        )}

        {resultUrl && (
          <div className="preview">
            <h3>Result</h3>
            <img src={resultUrl} alt="Result" />
            <button onClick={handleDownload} className="btn-secondary">
              Download Image
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
