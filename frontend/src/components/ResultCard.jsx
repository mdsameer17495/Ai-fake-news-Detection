import React from 'react';
import { ShieldCheck, AlertOctagon, Info, Tag, Percent, AlertTriangle } from 'lucide-react';

export default function ResultCard({ result }) {
  if (!result) return null;

  const isReal = result.prediction === 'REAL';
  const isInvalid = result.prediction?.includes('INVALID') || result.status === 'invalid_input';

  let borderColor = 'border-rose-500/40 shadow-rose-500/10';
  let badgeColor = 'bg-rose-500/20 text-rose-400 border-rose-500/40 shadow-rose-500/20';
  let bgGlow = 'bg-rose-500/10';

  if (isReal) {
    borderColor = 'border-emerald-500/40 shadow-emerald-500/10';
    badgeColor = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40 shadow-emerald-500/20';
    bgGlow = 'bg-emerald-500/10';
  } else if (isInvalid) {
    borderColor = 'border-amber-500/40 shadow-amber-500/10';
    badgeColor = 'bg-amber-500/20 text-amber-400 border-amber-500/40 shadow-amber-500/20';
    bgGlow = 'bg-amber-500/10';
  }

  return (
    <section id="prediction-result" className="py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className={`glass-panel rounded-2xl p-6 sm:p-8 border shadow-2xl relative overflow-hidden transition-all ${borderColor}`}>
          
          <div className={`absolute top-0 right-0 w-64 h-64 rounded-full blur-3xl pointer-events-none ${bgGlow}`} />

          <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <span className="text-xs font-bold uppercase tracking-widest text-slate-400">
              News Verification Final Verdict
            </span>
            <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">
              Logistic Regression + NewsAPI
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            
            {/* Verdict Badge */}
            <div className="flex flex-col items-start md:col-span-1">
              <span className="text-xs font-medium text-slate-400 mb-1">Final Result</span>
              <div className={`inline-flex items-center gap-2.5 px-4 py-2.5 rounded-xl font-black text-lg tracking-wider shadow-lg border ${badgeColor}`}>
                {isReal ? (
                  <ShieldCheck className="h-6 w-6 shrink-0" />
                ) : isInvalid ? (
                  <AlertTriangle className="h-6 w-6 shrink-0" />
                ) : (
                  <AlertOctagon className="h-6 w-6 shrink-0" />
                )}
                <span>{result.prediction}</span>
              </div>
            </div>

            {/* Confidence Score Meter (for valid news) */}
            {!isInvalid ? (
              <div className="flex flex-col">
                <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
                  <span className="flex items-center gap-1"><Percent className="h-3.5 w-3.5" /> ML Model Confidence</span>
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
            ) : (
              <div className="flex flex-col text-xs text-amber-300 bg-amber-500/10 p-3 rounded-xl border border-amber-500/20 font-medium">
                Invalid news input format. Conversational phrases and random gibberish cannot be evaluated as news articles.
              </div>
            )}

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

          {/* Decision Summary Reasons */}
          {result.reasons && result.reasons.length > 0 && (
            <div className="mt-6 pt-4 border-t border-slate-800/80">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">
                Verification Rationale:
              </span>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {result.reasons.map((r, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-blue-400 font-bold mt-0.5">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* AI Model Disclaimer */}
          <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-start gap-2.5 text-xs text-slate-400">
            <Info className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
            <p className="leading-relaxed">
              {result.disclaimer || "Final verdict requires both ML classifier structural alignment and live trusted news source verification."}
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
