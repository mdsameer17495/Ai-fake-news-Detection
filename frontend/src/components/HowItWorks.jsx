import React from 'react';
import { Upload, Cpu, BarChart3, Globe } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      num: "01",
      icon: <Upload className="h-6 w-6 text-blue-400" />,
      title: "Enter or Upload News",
      desc: "Paste your news text directly or upload a news image/screenshot for automated OCR text extraction."
    },
    {
      num: "02",
      icon: <Cpu className="h-6 w-6 text-indigo-400" />,
      title: "AI Feature Processing",
      desc: "Text is cleaned, transformed into a numerical matrix via TF-IDF vectorization, and tokenized."
    },
    {
      num: "03",
      icon: <BarChart3 className="h-6 w-6 text-purple-400" />,
      title: "Logistic Regression Predicts",
      desc: "Trained Logistic Regression model evaluates TF-IDF feature weights to output Fake/Real probability & confidence."
    },
    {
      num: "04",
      icon: <Globe className="h-6 w-6 text-emerald-400" />,
      title: "Trusted Source Verification",
      desc: "Extracted article keywords query live news APIs (Reuters, BBC, AP) to find corroborating live reports."
    }
  ];

  return (
    <section id="how-it-works" className="py-16 bg-slate-900/50 border-y border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-3xl font-bold text-white tracking-tight">How It Works</h2>
          <p className="mt-3 text-slate-400 text-sm sm:text-base">
            A transparent 4-step workflow combining machine learning text classification with real-time news source verification.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((s, idx) => (
            <div key={idx} className="glass-card rounded-xl p-6 relative flex flex-col justify-between hover:border-slate-700 transition-all">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                    {s.icon}
                  </div>
                  <span className="text-2xl font-black text-slate-700 font-mono">{s.num}</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{s.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
