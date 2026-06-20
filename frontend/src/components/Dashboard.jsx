import { motion } from 'framer-motion'
import EmptyState from './EmptyState'
import MetricCard from './MetricCard'
import CandidateTable from './CandidateTable'
import { Users, TrendingUp, Trophy, Brain } from 'lucide-react'

export default function Dashboard({ results, loading }) {
  if (loading) return <LoadingSkeleton />

  if (!results) return (
    <div className="flex-1 flex items-center justify-center">
      <EmptyState />
    </div>
  )

  const avg = (results.reduce((s, r) => s + r.score, 0) / results.length).toFixed(1)
  const top = results[0]
  const skillsFound = [...new Set(results.flatMap(r =>
    r.summary.match(/\b(Python|AWS|Azure|React|Node|SQL|Docker|API|ML|AI|Java|Cloud)\b/gi) || []
  ))].slice(0, 6)

  return (
    <main className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-4 gap-4">
        <MetricCard icon={Users} label="Candidates" value={results.length} color="primary" />
        <MetricCard icon={TrendingUp} label="Avg Match" value={`${avg}%`} color="accent" />
        <MetricCard icon={Trophy} label="Top Score" value={`${top.score}%`} color="success" />
        <MetricCard icon={Brain} label="Skills Found" value={skillsFound.length} color="warning" />
      </motion.div>

      {skillsFound.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="flex flex-wrap gap-2">
          <span className="text-[12px] text-muted mr-1 self-center">Skills detected:</span>
          {skillsFound.map(skill => (
            <span key={skill} className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-primary/15 text-primary border border-primary/20">{skill}</span>
          ))}
        </motion.div>
      )}

      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <CandidateTable results={results} />
      </motion.div>
    </main>
  )
}

function LoadingSkeleton() {
  return (
    <main className="flex-1 p-6 flex flex-col gap-6">
      <div className="grid grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-24 rounded-2xl bg-card border border-white/[0.06] animate-pulse" />
        ))}
      </div>
      <div className="h-64 rounded-2xl bg-card border border-white/[0.06] animate-pulse" />
    </main>
  )
}