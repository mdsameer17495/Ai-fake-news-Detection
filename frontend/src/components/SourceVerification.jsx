import React, { useState, useEffect } from 'react';
import { Globe, ExternalLink, Loader2, AlertCircle, Search, CheckCircle } from 'lucide-react';
import { verifyNewsSources } from '../services/api';

export default function SourceVerification({ articleText, initialData }) {
  const [loading, setLoading] = useState(false);
  const [verificationData, setVerificationData] = useState(initialData || null);

  useEffect(() => {
    if (initialData) {
      setVerificationData(initialData);
    } else if (articleText) {
      handleVerify(articleText);
    }
  }, [articleText, initialData]);

  const handleVerify = async (textToVerify) => {
    setLoading(true);
    try {
      const res = await verifyNewsSources(textToVerify);
      setVerificationData(res);
    } catch (err) {
      setVerificationData({
        status: 'error',
        message: 'Could not contact live verification service.',
        articles: []
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="trusted-sources" className="py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl">
          
          <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
                <Globe className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Trusted Source Verification</h3>
                <p className="text-xs text-slate-400">Independent live news API query & external article matching</p>
              </div>
            </div>

            {loading && (
              <span className="flex items-center gap-2 text-xs text-blue-400 font-mono">
                <Loader2 className="h-4 w-4 animate-spin" /> Searching News API...
              </span>
            )}
          </div>

          {/* Verification Result Display */}
          {verificationData && (
            <div>
              {/* Unconfigured State Banner */}
              {verificationData.status === 'unconfigured' && (
                <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm flex items-start gap-3 mb-4">
                  <AlertCircle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold block mb-0.5">Live Source Verification Unconfigured</span>
                    <span>{verificationData.message}</span>
                  </div>
                </div>
              )}

              {/* No Matches Found Banner */}
              {verificationData.status === 'no_matches' && (
                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-sm flex items-center gap-3 mb-4">
                  <Search className="h-5 w-5 text-slate-400 shrink-0" />
                  <span>No matching reports found across trusted news indices for these keywords.</span>
                </div>
              )}

              {/* Matching Articles List */}
              {verificationData.status === 'matches_found' && verificationData.articles.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-emerald-400" /> Similar Reports Found ({verificationData.articles.length})
                  </h4>

                  <div className="space-y-4">
                    {verificationData.articles.map((art, idx) => (
                      <div key={idx} className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between gap-3">
                        <div>
                          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
                            <span className="font-semibold text-blue-400">{art.source}</span>
                            <span className="font-mono">{art.publishedAt}</span>
                          </div>
                          <h5 className="text-sm font-bold text-white mb-1.5">{art.title}</h5>
                          <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{art.snippet}</p>
                        </div>

                        {art.url && art.url !== '#' && (
                          <a
                            href={art.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 font-semibold self-start transition-colors"
                          >
                            Open Full Article <ExternalLink className="h-3.5 w-3.5" />
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </section>
  );
}
