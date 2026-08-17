import React from 'react';
import { ArrowRight, ShieldCheck, Sparkles, FileText, Image as ImageIcon, Cpu, CheckSquare } from 'lucide-react';

export default function Hero({ onVerifyClick }) {
  return (
    <section id="hero" className="relative overflow-hidden pt-12 pb-16 lg:pt-20 lg:pb-24">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none animate-pulse-glow" />
      <div className="absolute top-1/3 right-10 w-72 h-72 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
          <Sparkles className="h-3.5 w-3.5" /> TF-IDF + Logistic Regression Machine Learning Architecture
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
          AI-Powered <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">Fake News Detection</span> & Verification
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed">
          Analyze news content, detect potential misinformation, and verify it using trusted sources.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            onClick={onVerifyClick}
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-base shadow-lg shadow-blue-600/30 transition-all flex items-center justify-center gap-2 group cursor-pointer"
          >
            Verify News
            <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {/* Visual Pipeline Flowchart */}
        <div className="mt-14 max-w-4xl mx-auto glass-panel rounded-2xl p-6 sm:p-8 shadow-2xl border border-slate-800">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-6">Execution Pipeline Overview</p>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-center">
            
            <div className="bg-slate-900/90 p-4 rounded-xl border border-slate-800 flex flex-col items-center text-center">
              <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-lg mb-2">
                <FileText className="h-5 w-5" />
              </div>
              <span className="text-xs font-semibold text-slate-200">Text / Image</span>
              <span className="text-[10px] text-slate-400">Raw Article / OCR</span>
            </div>

            <div className="hidden md:flex justify-center text-slate-500 font-mono text-xs">→</div>

            <div className="bg-slate-900/90 p-4 rounded-xl border border-slate-800 flex flex-col items-center text-center">
              <div className="p-2.5 bg-indigo-500/10 text-indigo-400 rounded-lg mb-2">
                <Cpu className="h-5 w-5" />
              </div>
              <span className="text-xs font-semibold text-slate-200">AI Analysis</span>
              <span className="text-[10px] text-slate-400">TF-IDF + Logistic Reg</span>
            </div>

            <div className="hidden md:flex justify-center text-slate-500 font-mono text-xs">→</div>

            <div className="bg-slate-900/90 p-4 rounded-xl border border-slate-800 flex flex-col items-center text-center">
              <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-lg mb-2">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <span className="text-xs font-semibold text-slate-200">Fake / Real Result</span>
              <span className="text-[10px] text-slate-400">+ Trusted Sources</span>
            </div>

          </div>
        </div>
      </div>
    </section>
  );
}
