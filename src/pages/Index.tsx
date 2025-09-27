import { useState } from "react";
import { MedicalAnalyzer } from "@/components/MedicalAnalyzer";
import { ResultsDisplay } from "@/components/ResultsDisplay";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Heart, ShieldCheck, FileText, LogOut, User } from "lucide-react";
import heroImage from "@/assets/hero-medical.jpg";

export interface AnalysisResult {
  keyFindings: string[];
  explanations: string[];
  recommendations: string[];
  urgentCare: string[];
  medicationDetails: {
    name: string;
    purpose: string;
    instructions: string;
    sideEffects?: string;
  }[];
  riskLevel: 'low' | 'moderate' | 'high';
}

const Index = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { user, logout } = useAuth();

  const handleAnalyzeReport = async (reportText: string, fileName?: string) => {
    setIsAnalyzing(true);
    
    try {
      // Call the Flask API for real AI analysis
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          reportText: reportText,
          filename: fileName
        })
      });
      
      const result = await response.json();
      
      if (result.status === 'success') {
        setAnalysisResult(result.data);
      } else {
        console.log('Analysis failed this:', result.error);
        console.error('Analysis failed:', result.error);
        // Fallback to mock data if API fails
        const fallbackResult: AnalysisResult = {
          keyFindings: [
            "Unable to analyze report at this time",
            "Please try again or contact support"
          ],
          explanations: [
            "The AI analysis service is temporarily unavailable",
            "This is a technical issue and does not reflect on your health status"
          ],
          recommendations: [
            "Try uploading your report again",
            "Contact your healthcare provider for analysis",
            "Keep a copy of your report for your records"
          ],
          urgentCare: [
            "If you have urgent health concerns, contact your doctor immediately"
          ],
          medicationDetails: [],
          riskLevel: 'moderate'
        };
        setAnalysisResult(fallbackResult);
      }
    } catch (error) {
      console.error('Error analyzing report:', error);
      // Fallback to mock data if network error
      const fallbackResult: AnalysisResult = {
        keyFindings: [
          "Network error occurred during analysis",
          "Please check your connection and try again"
        ],
        explanations: [
          "Unable to connect to the analysis service",
          "This is a temporary network issue"
        ],
        recommendations: [
          "Check your internet connection",
          "Try again in a few moments",
          "Contact your healthcare provider if urgent"
        ],
        urgentCare: [
          "If you have urgent health concerns, contact your doctor immediately"
        ],
        medicationDetails: [],
        riskLevel: 'moderate'
      };
      setAnalysisResult(fallbackResult);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background to-medical-light">
      {/* Header with User Info and Logout */}
      <header className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2 text-primary">
              <Heart className="h-6 w-6" />
              <span className="text-lg font-semibold">HealthTranslate</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user?.email}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={logout}
                className="flex items-center gap-2"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="flex items-center gap-2 text-primary">
                <Heart className="h-8 w-8" />
                <span className="text-xl font-semibold">HealthTranslate</span>
              </div>
              
              <div className="space-y-6">
                <h1 className="text-4xl md:text-6xl font-bold text-foreground leading-tight">
                  Understand Your
                  <span className="block bg-gradient-hero bg-clip-text text-transparent">
                    Medical Reports
                  </span>
                </h1>
                
                <p className="text-xl text-muted-foreground leading-relaxed max-w-lg">
                  Transform complex medical jargon into clear, easy-to-understand explanations. 
                  Get insights about your health in plain language.
                </p>
              </div>

              <div className="flex flex-wrap gap-6">
                <div className="flex items-center gap-3">
                  <ShieldCheck className="h-5 w-5 text-success" />
                  <span className="text-sm text-muted-foreground">HIPAA Compliant</span>
                </div>
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-accent" />
                  <span className="text-sm text-muted-foreground">AI-Powered Analysis</span>
                </div>
              </div>
            </div>

            <div className="relative">
              <img 
                src={heroImage} 
                alt="Medical professional reviewing health reports"
                className="rounded-2xl shadow-2xl object-cover w-full h-[500px]"
              />
              <div className="absolute inset-0 bg-gradient-hero opacity-10 rounded-2xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Application */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <MedicalAnalyzer onAnalyze={handleAnalyzeReport} isAnalyzing={isAnalyzing} />
          
          {analysisResult && (
            <ResultsDisplay result={analysisResult} />
          )}
        </div>
      </section>

      {/* Disclaimer */}
      <footer className="bg-card border-t border-border py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-warning/10 border border-warning/20 rounded-lg p-6">
            <p className="text-sm text-foreground leading-relaxed">
              <strong>Medical Disclaimer:</strong> This explanation is for understanding purposes only and does not replace professional medical advice. 
              Always consult your doctor or healthcare provider for personalized guidance and treatment decisions.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
};

export default Index;