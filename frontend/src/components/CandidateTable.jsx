import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, Medal } from 'lucide-react'

function ScoreBar({ score }) {
  const color = score >= 70 ? '#22C55E' : score >= 40 ? '#F59E0B' : '#EF4444'
  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          style={{ background: color }}
          className="h-full rounded-full"
        />
      </div>
      <span className="text-[13px] font-semibold w-12 text-right" style={{ color }}>{score}%</span>
    </div>
  )
}

function RankBadge({ rank }) {
  if (rank === 1) return <Medal size={18} className="text-warning" />
  return <span className="w-6 h-6 rounded-full bg-white/[0.06] flex items-center justify-center text-[11px] font-bold text-muted">{rank}</span>
}

function getRecommendation(score) {
  if (score >= 70) return { label: 'Strong Match', color: 'text-success bg-success/15 border-success/25' }
  if (score >= 45) return { label: 'Potential Fit', color: 'text-warning bg-warning/15 border-warning/25' }
  return { label: 'Low Match', color: 'text-danger bg-danger/15 border-danger/25' }
}

export default function CandidateTable({ results }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="bg-card border border-white/[0.06] rounded-2xl overflow-hidden">
      <div className="px-5 py-4 border-b border-white/[0.06] flex items-center justify-between">
        <h3 className="text-[15px] font-semibold text-white">Candidate Rankings</h3>
        <span className="text-[12px] text-muted">{results.length} candidates analyzed</span>
      </div>

      <div className="grid grid-cols-12 gap-4 px-5 py-3 border-b border-white/[0.04] text-[11px] font-semibold text-muted uppercase tracking-wider">
        <div className="col-span-1">Rank</div>
        <div className="col-span-3">Candidate</div>
        <div className="col-span-4">Match Score</div>
        <div className="col-span-2">Recommendation</div>
        <div className="col-span-2 text-right">Summary</div>
      </div>

      {results.map((r, i) => {
        const rec = getRecommendation(r.score)
        const isOpen = expanded === r.candidate
        return (
          <motion.div key={r.candidate} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.07 }}>
            <div
              className="grid grid-cols-12 gap-4 px-5 py-4 border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors cursor-pointer items-center"
              onClick={() => setExpanded(isOpen ? null : r.candidate)}
            >
              <div className="col-span-1 flex items-center"><RankBadge rank={r.rank} /></div>
              <div className="col-span-3"><p className="text-[13px] font-medium text-white truncate">{r.candidate.replace('.pdf', '')}</p></div>
              <div className="col-span-4"><ScoreBar score={r.score} /></div>
              <div className="col-span-2">
                <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full border ${rec.color}`}>{rec.label}</span>
              </div>
              <div className="col-span-2 flex justify-end">
                <button className="text-muted hover:text-white transition-colors">
                  {isOpen ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
                </button>
              </div>
            </div>

            <AnimatePresence>
              {isOpen && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }} className="overflow-hidden">
                  <div className="px-5 py-4 bg-surface/50 border-b border-white/[0.04]">
                    <p className="text-[12px] font-semibold text-muted uppercase tracking-wider mb-2">AI Summary</p>
                    <p className="text-[13px] text-white/80 leading-relaxed">{r.summary}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )
      })}
    </div>
  )
}