import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 py-10 text-xs text-slate-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        
        <div className="flex items-center gap-2">
          <ShieldAlert className="h-5 w-5 text-blue-500" />
          <span className="font-semibold text-slate-300">VeriTruth AI</span>
          <span>— College AI/ML Capstone Project</span>
        </div>

        <p className="text-slate-500">
          Built with Python FastAPI, scikit-learn (TF-IDF + Logistic Regression), Tesseract OCR, and React.
        </p>
      </div>
    </footer>
  );
}
