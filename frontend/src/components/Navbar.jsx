import { Search, Settings, Bell } from 'lucide-react'
import { motion } from 'framer-motion'

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="h-[72px] flex items-center justify-between px-6 border-b border-white/[0.06] bg-surface/80 backdrop-blur-md sticky top-0 z-50"
    >
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
          <span className="text-white font-bold text-sm">S</span>
        </div>
        <span className="text-white font-semibold text-[15px] tracking-tight">
          Siemens AI Screener
        </span>
        <span className="ml-2 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-primary/15 text-primary border border-primary/25">
          BETA
        </span>
      </div>
      <div className="flex items-center gap-2">
        <button className="w-9 h-9 flex items-center justify-center rounded-lg text-muted hover:text-white hover:bg-white/[0.06] transition-all">
          <Search size={16} />
        </button>
        <button className="w-9 h-9 flex items-center justify-center rounded-lg text-muted hover:text-white hover:bg-white/[0.06] transition-all">
          <Bell size={16} />
        </button>
        <button className="w-9 h-9 flex items-center justify-center rounded-lg text-muted hover:text-white hover:bg-white/[0.06] transition-all">
          <Settings size={16} />
        </button>
        <div className="ml-2 w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white text-xs font-bold">
          AB
        </div>
      </div>
    </motion.nav>
  )
}