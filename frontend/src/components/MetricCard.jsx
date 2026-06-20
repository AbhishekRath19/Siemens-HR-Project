import { motion } from 'framer-motion'

const colorMap = {
  primary: 'text-primary bg-primary/15 border-primary/20',
  accent:  'text-accent bg-accent/15 border-accent/20',
  success: 'text-success bg-success/15 border-success/20',
  warning: 'text-warning bg-warning/15 border-warning/20',
}

export default function MetricCard({ icon: Icon, label, value, color }) {
  return (
    <motion.div
      whileHover={{ y: -2, boxShadow: '0 8px 30px rgba(0,0,0,0.3)' }}
      className="bg-card border border-white/[0.06] rounded-2xl p-4 flex flex-col gap-3"
    >
      <div className={`w-9 h-9 rounded-xl border flex items-center justify-center ${colorMap[color]}`}>
        <Icon size={16} />
      </div>
      <div>
        <p className="text-2xl font-bold text-white">{value}</p>
        <p className="text-[12px] text-muted mt-0.5">{label}</p>
      </div>
    </motion.div>
  )
}