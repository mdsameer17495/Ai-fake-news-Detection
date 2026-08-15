import React, { useState } from 'react';
import { FileText, Image as ImageIcon, Upload, Loader2, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { predictTextNews, predictImageNews } from '../services/api';

export default function VerifySection({ onAnalysisComplete }) {
  const [activeTab, setActiveTab] = useState('text'); // 'text' | 'image'
  
  // Text Mode state
  const [textInput, setTextInput] = useState('');
  const [textError, setTextError] = useState('');

  // Image Mode state
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [imageError, setImageError] = useState('');

  // General loading & OCR state
  const [loading, setLoading] = useState(false);
  const [extractedText, setExtractedText] = useState('');
  const [apiError, setApiError] = useState('');

  const handleTextAnalyze = async () => {
    setTextError('');
    setApiError('');
    if (!textInput.trim() || textInput.trim().split(/\s+/).length < 5) {
      setTextError('Please enter a sufficient news article (at least 5 words).');
      return;
    }

    setLoading(true);
    try {
      const data = await predictTextNews(textInput.trim());
      onAnalysisComplete({
        inputMode: 'text',
        articleText: textInput.trim(),
        prediction: data.prediction,
        confidence: data.confidence,
        category: data.category,
        signals: data.signals,
        reasons: data.reasons,
        verification_data: data.verification_data,
        verified_articles: data.verified_articles,
        disclaimer: data.disclaimer
      });
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to analyze news text. Ensure backend is running.';
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (file) => {
    setImageError('');
    setApiError('');
    if (!file) return;

    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
      setImageError('Unsupported image format. Please upload JPG, JPEG, or PNG.');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setImageError('File size exceeds the 5 MB maximum limit.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleImageAnalyze = async () => {
    setImageError('');
    setApiError('');
    if (!selectedFile) {
      setImageError('Please select a news image to analyze.');
      return;
    }

    setLoading(true);
    setExtractedText('');

    try {
      const data = await predictImageNews(selectedFile);
      setExtractedText(data.extracted_text);

      const res = data.prediction_result;
      onAnalysisComplete({
        inputMode: 'image',
        extractedText: data.extracted_text,
        articleText: data.extracted_text,
        prediction: res.prediction,
        confidence: res.confidence,
        category: res.category,
        signals: res.signals,
        reasons: res.reasons,
        verification_data: res.verification_data,
        verified_articles: res.verified_articles,
        disclaimer: res.disclaimer
      });
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to extract or analyze news image.';
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleClearText = () => {
    setTextInput('');
    setTextError('');
    setApiError('');
  };

  const handleClearImage = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setImageError('');
    setExtractedText('');
    setApiError('');
  };

  return (
    <section id="verify" className="py-16 relative">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white tracking-tight">Choose how you want to verify the news</h2>
          <p className="mt-2 text-slate-400 text-sm">Select your news input format below to run machine learning prediction.</p>
        </div>

        {/* Tab Selector Buttons */}
        <div className="flex items-center justify-center gap-4 mb-8">
          <button
            onClick={() => setActiveTab('text')}
            className={`px-6 py-3 rounded-xl font-medium text-sm flex items-center gap-2.5 transition-all cursor-pointer ${
              activeTab === 'text'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30 border border-blue-500'
                : 'bg-slate-900/90 text-slate-400 border border-slate-800 hover:text-white'
            }`}
          >
            <FileText className="h-4 w-4" /> 📝 Verify Text
          </button>

          <button
            onClick={() => setActiveTab('image')}
            className={`px-6 py-3 rounded-xl font-medium text-sm flex items-center gap-2.5 transition-all cursor-pointer ${
              activeTab === 'image'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30 border border-blue-500'
                : 'bg-slate-900/90 text-slate-400 border border-slate-800 hover:text-white'
            }`}
          >
            <ImageIcon className="h-4 w-4" /> 🖼️ Verify Image
          </button>
        </div>

        {/* API Level Error Banner */}
        {apiError && (
          <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold block mb-0.5">Analysis Failed</span>
              <span>{apiError}</span>
            </div>
          </div>
        )}

        {/* MODE 1: TEXT NEWS */}
        {activeTab === 'text' && (
          <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl">
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Paste your news article
            </label>
            
            <textarea
              rows={8}
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Paste the complete news article here..."
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all resize-y"
            />

            {textError && (
              <p className="mt-2 text-xs text-rose-400 flex items-center gap-1.5 font-medium">
                <AlertTriangle className="h-3.5 w-3.5" /> {textError}
              </p>
            )}

            <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
              <span className="text-xs text-slate-400 font-mono">
                Words: {textInput.trim() ? textInput.trim().split(/\s+/).length : 0}
              </span>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={handleClearText}
                  disabled={loading}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors cursor-pointer"
                >
                  Clear
                </button>

                <button
                  type="button"
                  onClick={handleTextAnalyze}
                  disabled={loading}
                  className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold shadow-lg shadow-blue-600/25 transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" /> Analyzing Article...
                    </>
                  ) : (
                    'Analyze News'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* MODE 2: IMAGE NEWS */}
        {activeTab === 'image' && (
          <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl">
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                  handleImageChange(e.dataTransfer.files[0]);
                }
              }}
              className="border-2 border-dashed border-slate-700 hover:border-blue-500/70 rounded-2xl p-8 text-center transition-all bg-slate-950/40 relative cursor-pointer"
            >
              <input
                type="file"
                accept="image/jpeg, image/jpg, image/png"
                onChange={(e) => e.target.files && handleImageChange(e.target.files[0])}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />

              {previewUrl ? (
                <div className="flex flex-col items-center">
                  <img src={previewUrl} alt="Preview" className="max-h-48 rounded-lg border border-slate-700 shadow-md mb-3 object-contain" />
                  <p className="text-xs text-slate-300 font-mono">{selectedFile?.name}</p>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center">
                  <div className="p-4 bg-slate-900 rounded-full border border-slate-800 mb-3 text-blue-400">
                    <Upload className="h-8 w-8" />
                  </div>
                  <h3 className="text-base font-semibold text-slate-200">Upload a news image</h3>
                  <p className="text-xs text-slate-400 mt-1">Supported formats: JPG, JPEG, PNG (Hindi + English OCR)</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">Maximum file size: 5 MB</p>
                </div>
              )}
            </div>

            {imageError && (
              <p className="mt-3 text-xs text-rose-400 flex items-center gap-1.5 font-medium">
                <AlertTriangle className="h-3.5 w-3.5" /> {imageError}
              </p>
            )}

            <div className="mt-6 flex items-center justify-end gap-3">
              {selectedFile && (
                <button
                  type="button"
                  onClick={handleClearImage}
                  disabled={loading}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors cursor-pointer"
                >
                  Clear Image
                </button>
              )}

              <button
                type="button"
                onClick={handleImageAnalyze}
                disabled={loading || !selectedFile}
                className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold shadow-lg shadow-blue-600/25 transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> OCR & Analyzing...
                  </>
                ) : (
                  'Analyze Image'
                )}
              </button>
            </div>

            {/* OCR Extracted Text Display */}
            {extractedText && (
              <div className="mt-8 p-4 bg-slate-950 border border-slate-800 rounded-xl">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" /> Extracted Text (OCR)
                </div>
                <p className="text-xs text-slate-300 font-mono bg-slate-900/80 p-3 rounded border border-slate-800 leading-relaxed max-h-36 overflow-y-auto">
                  {extractedText}
                </p>
              </div>
            )}

          </div>
        )}

      </div>
    </section>
  );
}
