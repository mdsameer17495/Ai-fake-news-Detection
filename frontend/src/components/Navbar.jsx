import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function Navbar({ healthStatus }) {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <ShieldAlert className="h-6 w-6 text-white" />
          </div>
          <div>
            <span className="font-bold text-lg text-white tracking-wide flex items-center gap-2">
              VeriTruth <span className="text-xs bg-blue-500/20 text-blue-400 font-semibold px-2 py-0.5 rounded-full border border-blue-500/30">AI ML Project</span>
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
          <a href="#hero" className="hover:text-blue-400 transition-colors">Home</a>
          <a href="#how-it-works" className="hover:text-blue-400 transition-colors">How It Works</a>
          <a href="#verify" className="hover:text-blue-400 transition-colors">Verify News</a>
        </nav>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 text-xs">
            <span className={`h-2 w-2 rounded-full ${healthStatus?.online ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
            <span className="text-slate-300 font-mono">
              {healthStatus?.online ? 'API Online' : 'Connecting API...'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
