import { motion } from 'framer-motion'
import { FileSearch } from 'lucide-react'

const steps = [
  { n: '01', label: 'Paste job description', desc: 'Add the full JD in the sidebar' },
  { n: '02', label: 'Upload PDF resumes', desc: 'Drag & drop or click to browse' },
  { n: '03', label: 'Click Analyze', desc: 'AI ranks candidates instantly' },
]

export default function EmptyState() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center gap-8 max-w-lg text-center px-6"
    >
      <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-primary/30 to-accent/20 border border-primary/20 flex items-center justify-center">
        <FileSearch size={36} className="text-primary" />
      </div>
      <div>
        <h2 className="text-2xl font-bold text-white mb-3">Ready to Screen Candidates</h2>
        <p className="text-muted text-[15px] leading-relaxed">
          AI-powered semantic matching that goes beyond keywords — understanding the actual meaning of resumes and job requirements.
        </p>
      </div>
      <div className="grid grid-cols-3 gap-4 w-full">
        {steps.map((s, i) => (
          <motion.div
            key={s.n}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * i + 0.3 }}
            className="bg-card border border-white/[0.06] rounded-2xl p-4 flex flex-col gap-2"
          >
            <span className="text-primary font-bold text-[13px]">{s.n}</span>
            <span className="text-white font-semibold text-[13px]">{s.label}</span>
            <span className="text-muted text-[11px] leading-relaxed">{s.desc}</span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}