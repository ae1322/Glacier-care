import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle, AlertTriangle, AlertCircle, Heart, Lightbulb, Phone, Pill } from "lucide-react";
import { AnalysisResult } from "@/pages/Index";

interface ResultsDisplayProps {
  result: AnalysisResult;
}

export const ResultsDisplay = ({ result }: ResultsDisplayProps) => {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'bg-success text-success-foreground';
      case 'moderate': return 'bg-warning text-warning-foreground';
      case 'high': return 'bg-destructive text-destructive-foreground';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'low': return <CheckCircle className="h-4 w-4" />;
      case 'moderate': return <AlertTriangle className="h-4 w-4" />;
      case 'high': return <AlertCircle className="h-4 w-4" />;
      default: return <Heart className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Risk Level Header */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-xl text-foreground">Analysis Complete</CardTitle>
              <CardDescription className="text-muted-foreground">
                Here's what your medical report means in simple terms
              </CardDescription>
            </div>
            <Badge className={`${getRiskColor(result.riskLevel)} flex items-center gap-2`}>
              {getRiskIcon(result.riskLevel)}
              {result.riskLevel.charAt(0).toUpperCase() + result.riskLevel.slice(1)} Risk
            </Badge>
          </div>
        </CardHeader>
      </Card>

      {/* Urgent Care Alerts */}
      {result.urgentCare.length > 0 && (
        <Alert className="border-warning bg-warning/5">
          <Phone className="h-4 w-4" />
          <AlertDescription>
            <div className="font-medium mb-2">When to Contact Your Doctor:</div>
            <ul className="space-y-1">
              {result.urgentCare.map((item, index) => (
                <li key={index} className="text-sm">• {item}</li>
              ))}
            </ul>
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Key Findings */}
        <Card className="bg-card border-border">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Heart className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg">Key Findings</CardTitle>
            </div>
            <CardDescription>
              Important numbers and measurements from your report
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {result.keyFindings.map((finding, index) => (
                <li key={index} className="flex items-start gap-3 p-3 bg-secondary/50 rounded-lg">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <span className="text-sm text-foreground">{finding}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {/* Explanations */}
        <Card className="bg-card border-border">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lightbulb className="h-5 w-5 text-accent" />
              <CardTitle className="text-lg">What This Means</CardTitle>
            </div>
            <CardDescription>
              Simple explanations of your medical results
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {result.explanations.map((explanation, index) => (
                <li key={index} className="p-3 bg-medical-light rounded-lg">
                  <span className="text-sm text-foreground leading-relaxed">{explanation}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Medication Details */}
      {result.medicationDetails && result.medicationDetails.length > 0 && (
        <Card className="border-accent/20 bg-accent/5">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Pill className="h-5 w-5 text-accent" />
              <CardTitle className="text-lg text-accent">Your Medications Explained</CardTitle>
            </div>
            <CardDescription>
              Simple explanations of what your medicines do and how to take them
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {result.medicationDetails.map((med, index) => (
              <div key={index} className="border border-border rounded-lg p-4 space-y-3">
                <h4 className="font-semibold text-foreground text-base">{med.name}</h4>
                <div className="space-y-2">
                  <div>
                    <span className="text-sm font-medium text-accent">What it does: </span>
                    <span className="text-sm text-muted-foreground">{med.purpose}</span>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-accent">How to take it: </span>
                    <span className="text-sm text-muted-foreground">{med.instructions}</span>
                  </div>
                  {med.sideEffects && (
                    <div>
                      <span className="text-sm font-medium text-warning">Important notes: </span>
                      <span className="text-sm text-muted-foreground">{med.sideEffects}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <div className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-success" />
            <CardTitle className="text-lg">Recommendations</CardTitle>
          </div>
          <CardDescription>
            Steps you can take to improve or maintain your health
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2">
            {result.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start gap-3 p-4 bg-success/5 border border-success/20 rounded-lg">
                <CheckCircle className="h-4 w-4 text-success mt-0.5 flex-shrink-0" />
                <span className="text-sm text-foreground">{recommendation}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};