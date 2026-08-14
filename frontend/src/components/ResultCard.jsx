import React from 'react';
import { ShieldCheck, AlertOctagon, Info, Tag, Percent } from 'lucide-react';

export default function ResultCard({ result }) {
  if (!result) return null;

  const isReal = result.prediction === 'REAL';

  return (
    <section id="prediction-result" className="py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className={`glass-panel rounded-2xl p-6 sm:p-8 border shadow-2xl relative overflow-hidden transition-all ${
          isReal ? 'border-emerald-500/40 shadow-emerald-500/10' : 'border-rose-500/40 shadow-rose-500/10'
        }`}>
          
          {/* Subtle status backdrop highlight */}
          <div className={`absolute top-0 right-0 w-64 h-64 rounded-full blur-3xl pointer-events-none ${
            isReal ? 'bg-emerald-500/10' : 'bg-rose-500/10'
          }`} />

          <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <span className="text-xs font-bold uppercase tracking-widest text-slate-400">
              AI Prediction Analysis Result
            </span>
            <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">
              Logistic Regression
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            
            {/* Prediction Status Badge */}
            <div className="flex flex-col items-start">
              <span className="text-xs font-medium text-slate-400 mb-1">Prediction</span>
              <div className={`inline-flex items-center gap-2.5 px-5 py-2.5 rounded-xl font-black text-xl tracking-wider shadow-lg ${
                isReal 
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-emerald-500/20' 
                  : 'bg-rose-500/20 text-rose-400 border border-rose-500/40 shadow-rose-500/20'
              }`}>
                {isReal ? <ShieldCheck className="h-6 w-6" /> : <AlertOctagon className="h-6 w-6" />}
                {result.prediction}
              </div>
            </div>

            {/* Confidence Score Meter */}
            <div className="flex flex-col">
              <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
                <span className="flex items-center gap-1"><Percent className="h-3.5 w-3.5" /> Confidence</span>
                <span className="text-slate-200 font-bold font-mono">{result.confidence}%</span>
              </div>
              <div className="w-full h-3 bg-slate-950 rounded-full border border-slate-800 overflow-hidden p-0.5">
                <div 
                  className={`h-full rounded-full transition-all duration-1000 ${
                    isReal ? 'bg-emerald-500' : 'bg-rose-500'
                  }`} 
                  style={{ width: `${result.confidence}%` }}
                />
              </div>
            </div>

            {/* Category Tag */}
            <div className="flex flex-col md:items-end">
              <span className="text-xs font-medium text-slate-400 mb-1 flex items-center gap-1">
                <Tag className="h-3.5 w-3.5" /> Category
              </span>
              <span className="px-3.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-sm font-semibold text-blue-300">
                {result.category || 'General'}
              </span>
            </div>

          </div>

          {/* AI Model Disclaimer */}
          <div className="mt-8 pt-4 border-t border-slate-800/80 flex items-start gap-2.5 text-xs text-slate-400">
            <Info className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
            <p className="leading-relaxed">
              {result.disclaimer || "AI prediction is based on patterns learned from the training data and should not be treated as absolute proof of factual truth."}
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
