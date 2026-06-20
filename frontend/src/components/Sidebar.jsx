import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Sparkles, Upload, X, FileText, Loader2, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Sidebar({ jobDescription, setJobDescription, files, setFiles, onAnalyze, loading, error }) {
  const onDrop = useCallback(accepted => {
    setFiles(prev => {
      const names = prev.map(f => f.name)
      const newFiles = accepted.filter(f => !names.includes(f.name))
      return [...prev, ...newFiles]
    })
  }, [setFiles])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: true
  })

  const removeFile = name => setFiles(prev => prev.filter(f => f.name !== name))

  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="w-[320px] flex-shrink-0 border-r border-white/[0.06] bg-surface/50 flex flex-col p-5 gap-5 overflow-y-auto"
    >
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Sparkles size={15} className="text-primary" />
          <span className="text-[13px] font-semibold text-white">Job Description</span>
        </div>
        <textarea
          value={jobDescription}
          onChange={e => setJobDescription(e.target.value)}
          placeholder="Paste the full job description here. The AI will use this to evaluate and rank candidates semantically..."
          className="w-full h-52 bg-card border border-white/[0.08] rounded-xl p-3.5 text-[13px] text-white placeholder-muted/60 resize-none outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/25 transition-all leading-relaxed"
        />
        <div className="flex justify-between">
          <span className="text-[11px] text-muted">{jobDescription.length} characters</span>
          {jobDescription.length > 0 && <span className="text-[11px] text-success">Ready</span>}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Upload size={15} className="text-primary" />
          <span className="text-[13px] font-semibold text-white">Upload Resumes</span>
        </div>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-6 flex flex-col items-center gap-2 cursor-pointer transition-all
            ${isDragActive ? 'border-primary bg-primary/10' : 'border-white/[0.1] hover:border-primary/50 hover:bg-white/[0.02]'}`}
        >
          <input {...getInputProps()} />
          <div className="w-10 h-10 rounded-xl bg-primary/15 flex items-center justify-center">
            <Upload size={18} className="text-primary" />
          </div>
          <p className="text-[13px] text-white font-medium text-center">
            {isDragActive ? 'Drop files here...' : 'Drag & drop PDFs'}
          </p>
          <p className="text-[11px] text-muted text-center">or click to browse · PDF only</p>
        </div>

        <AnimatePresence>
          {files.map(file => (
            <motion.div
              key={file.name}
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="flex items-center gap-3 bg-card border border-white/[0.06] rounded-xl px-3 py-2.5"
            >
              <div className="w-7 h-7 rounded-lg bg-primary/15 flex items-center justify-center flex-shrink-0">
                <FileText size={13} className="text-primary" />
              </div>
              <span className="text-[12px] text-white truncate flex-1">{file.name}</span>
              <button onClick={() => removeFile(file.name)} className="text-muted hover:text-danger transition-colors">
                <X size={13} />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-start gap-2 bg-danger/10 border border-danger/25 rounded-xl p-3">
          <AlertCircle size={14} className="text-danger mt-0.5 flex-shrink-0" />
          <p className="text-[12px] text-danger">{error}</p>
        </motion.div>
      )}

      <motion.button
        onClick={onAnalyze}
        disabled={loading}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="mt-auto w-full py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-[14px] flex items-center justify-center gap-2 shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {loading ? (<><Loader2 size={16} className="animate-spin" />Analyzing...</>) : (<><Sparkles size={16} />Analyze Candidates</>)}
      </motion.button>
    </motion.aside>
  )
}