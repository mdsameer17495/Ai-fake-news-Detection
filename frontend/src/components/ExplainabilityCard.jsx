import React from 'react';
import { HelpCircle, CheckCircle2, Sparkles } from 'lucide-react';

export default function ExplainabilityCard({ result }) {
  if (!result || !result.reasons) return null;

  return (
    <section id="why-prediction" className="py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl">
          
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
              <HelpCircle className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">Why did the AI make this prediction?</h3>
              <p className="text-xs text-slate-400">Model explainability based on Logistic Regression feature coefficients and TF-IDF vectors</p>
            </div>
          </div>

          {/* Key Reasons List */}
          <div className="space-y-3 mb-6">
            {result.reasons.map((reason, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3.5 bg-slate-950/60 rounded-xl border border-slate-800">
                <CheckCircle2 className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
                <p className="text-sm text-slate-200 leading-relaxed">{reason}</p>
              </div>
            ))}
          </div>

          {/* Influential Signals / TF-IDF Vocabulary Tokens */}
          {result.signals && result.signals.length > 0 && (
            <div className="pt-4 border-t border-slate-800">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5 text-indigo-400" /> Important Influential Signals (TF-IDF Features)
              </span>
              <div className="flex flex-wrap gap-2 mt-2">
                {result.signals.map((word, i) => (
                  <span key={i} className="px-3 py-1 rounded-lg bg-indigo-950/50 border border-indigo-800/60 text-indigo-300 text-xs font-mono font-medium">
                    #{word}
                  </span>
                ))}
              </div>
            </div>
          )}

        </div>
      </div>
    </section>
  );
}
