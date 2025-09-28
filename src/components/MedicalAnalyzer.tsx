import { useState, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, FileText, Loader2, Camera, FileImage } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface MedicalAnalyzerProps {
  onAnalyze: (reportText: string, fileName?: string) => void;
  onFileAnalyze: (file: File) => void;
  isAnalyzing: boolean;
}

export const MedicalAnalyzer = ({ onAnalyze, onFileAnalyze, isAnalyzing }: MedicalAnalyzerProps) => {
  const [reportText, setReportText] = useState("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (uploadedFile && !reportText.includes('[IMAGE FILE]') && !reportText.includes('[DOCUMENT FILE]')) {
      // If we have a file and it's not already processed, send the file
      onFileAnalyze(uploadedFile);
    } else if (reportText.trim()) {
      // If we have text content, analyze it
      onAnalyze(reportText, uploadedFile?.name);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const maxSize = 20 * 1024 * 1024; // 20MB
    if (file.size > maxSize) {
      toast({
        title: "File too large",
        description: "Please select a file smaller than 20MB",
        variant: "destructive",
      });
      return;
    }

    const supportedTypes = [
      'application/pdf',
      'image/jpeg',
      'image/jpg', 
      'image/png',
      'image/webp',
      'text/plain',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];

    if (!supportedTypes.includes(file.type)) {
      toast({
        title: "Unsupported file type",
        description: "Please upload PDF, Image, or Text files",
        variant: "destructive",
      });
      return;
    }

    setUploadedFile(file);
    
    try {
      // For text files, read content directly
      if (file.type === 'text/plain') {
        const text = await file.text();
        setReportText(text);
        toast({
          title: "Text file loaded",
          description: `${file.name} content loaded for analysis`,
        });
      } else if (file.type.startsWith('image/')) {
        // For images, we'll send the file to the backend for processing
        setReportText(`[IMAGE FILE] ${file.name} - Ready for analysis`);
        toast({
          title: "Image uploaded",
          description: `${file.name} is ready for analysis`,
        });
      } else {
        // For PDF and DOC files, show filename and let backend handle it
        setReportText(`[DOCUMENT FILE] ${file.name} - Ready for analysis`);
        toast({
          title: "Document uploaded",
          description: `${file.name} is ready for analysis`,
        });
      }
    } catch (error) {
      console.error('Error reading file:', error);
      toast({
        title: "Error reading file",
        description: "Could not read the file content",
        variant: "destructive",
      });
    }
  };

  const clearFile = () => {
    setUploadedFile(null);
    setReportText("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const sampleTexts = [
    {
      title: "Blood Test Sample",
      content: "Hemoglobin: 9.8 g/dL (Normal: 12-16 g/dL)\nHematocrit: 32% (Normal: 36-46%)\nGlucose: 95 mg/dL (Normal: 70-100 mg/dL)\nTotal Cholesterol: 180 mg/dL (Normal: <200 mg/dL)"
    },
    {
      title: "Prescription Sample",
      content: "Tab. Metformin 500mg - Take 1 tablet twice daily after meals\nTab. Lisinopril 10mg - Take 1 tablet once daily in morning\nVitamin D3 1000 IU - Take 1 capsule daily"
    }
  ];

  return (
    <Card className="bg-gradient-card border-border/50 shadow-lg">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <FileText className="h-5 w-5 text-primary" />
          </div>
          <div>
            <CardTitle className="text-2xl text-foreground">Upload Your Medical Report</CardTitle>
            <CardDescription className="text-muted-foreground">
              Paste your medical report, lab results, or prescription details below
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* File Upload Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-foreground">
                Upload Medical Report
              </label>
              {uploadedFile && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={clearFile}
                  className="text-xs"
                >
                  Clear File
                </Button>
              )}
            </div>
            
            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
              <Input
                ref={fileInputRef}
                type="file"
                onChange={handleFileUpload}
                accept=".pdf,.jpg,.jpeg,.png,.webp,.txt,.doc,.docx"
                className="hidden"
                disabled={isAnalyzing}
              />
              
              {uploadedFile ? (
                <div className="space-y-2">
                  <div className="flex items-center justify-center gap-2 text-success">
                    <FileImage className="h-8 w-8" />
                  </div>
                  <p className="text-sm font-medium text-foreground">{uploadedFile.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-center gap-2 text-muted-foreground">
                    <Upload className="h-8 w-8" />
                    <Camera className="h-8 w-8" />
                  </div>
                  <div>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => fileInputRef.current?.click()}
                      disabled={isAnalyzing}
                    >
                      Choose File
                    </Button>
                    <p className="text-xs text-muted-foreground mt-2">
                      PDF, Image (JPG, PNG), or Text files (max 20MB)
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex-1 h-px bg-border"></div>
            <span className="text-xs text-muted-foreground">OR</span>
            <div className="flex-1 h-px bg-border"></div>
          </div>

          <div className="space-y-2">
            <label htmlFor="report-text" className="text-sm font-medium text-foreground">
              Type Medical Report Content
            </label>
            <Textarea
              id="report-text"
              placeholder="Example: Hemoglobin: 9.8 g/dL (Normal: 12-16 g/dL)..."
              value={reportText}
              onChange={(e) => setReportText(e.target.value)}
              className="min-h-[200px] resize-none bg-background border-border focus:border-primary"
              disabled={isAnalyzing}
            />
          </div>

          <Button 
            type="submit" 
            disabled={(!reportText.trim() && !uploadedFile) || isAnalyzing}
            className="w-full bg-gradient-hero hover:opacity-90 transition-opacity"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing Report...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Analyze Report
              </>
            )}
          </Button>
        </form>

        {/* Sample Data */}
        <div className="border-t border-border pt-6">
          <h3 className="text-sm font-medium text-foreground mb-3">Try with sample data:</h3>
          <div className="grid gap-3">
            {sampleTexts.map((sample, index) => (
              <button
                key={index}
                onClick={() => setReportText(sample.content)}
                className="text-left p-3 bg-secondary hover:bg-secondary/80 rounded-lg border border-border transition-colors"
                disabled={isAnalyzing}
              >
                <div className="text-sm font-medium text-foreground">{sample.title}</div>
                <div className="text-xs text-muted-foreground mt-1 truncate">
                  {sample.content.split('\n')[0]}...
                </div>
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};