import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import VerifySection from './components/VerifySection';
import ResultCard from './components/ResultCard';
import SourceVerification from './components/SourceVerification';
import Footer from './components/Footer';
import { checkHealth } from './services/api';

export default function App() {
  const [health, setHealth] = useState(null);
  const [currentResult, setCurrentResult] = useState(null);

  useEffect(() => {
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const data = await checkHealth();
      setHealth({ online: true, ...data });
    } catch (e) {
      setHealth({ online: false });
    }
  };

  const scrollToVerify = () => {
    document.getElementById('verify')?.scrollIntoView({ behavior: 'smooth' });
  };

  const scrollToHowItWorks = () => {
    document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleAnalysisComplete = (resultData) => {
    setCurrentResult(resultData);
    
    // Smooth scroll down to prediction result
    setTimeout(() => {
      document.getElementById('prediction-result')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar healthStatus={health} />
      
      <main className="flex-grow">
        <Hero onVerifyClick={scrollToVerify} onHowItWorksClick={scrollToHowItWorks} />
        
        <HowItWorks />
        
        <VerifySection onAnalysisComplete={handleAnalysisComplete} />
        
        {currentResult && (
          <>
            <ResultCard result={currentResult} />
            <SourceVerification 
              articleText={currentResult.articleText || currentResult.extractedText} 
              initialData={currentResult.verification_data} 
            />
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
