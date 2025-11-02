import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useTheme } from "@/contexts/ThemeContext";
import { Moon, Sun, FileText, Download, Search, X, Columns3, List } from "lucide-react";
import { useState, useMemo, useRef, useEffect } from "react";
import { trpc } from "@/lib/trpc";
import jsPDF from "jspdf";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { CommentDialog } from "@/components/CommentDialog";
import { 
  getSeverityColor, 
  getSeverityBadgeColor, 
  getEvidenceColor, 
  getEvidenceBadgeColor 
} from "@/lib/colorUtils";

interface ParagraphData {
  content: string;
  summary?: string | null;
  severity?: number | null;
  evidenceStrength?: number | null;
  annexures?: string[];
}

interface AffidavitSection {
  title: string;
  paragraphs: Record<string, ParagraphData>;
  jr_responses?: Record<string, ParagraphData>;
  dr_responses?: Record<string, ParagraphData>;
}

interface AffidavitData {
  [key: string]: AffidavitSection;
}

type ViewMode = "columns" | "grouped";

export default function Home() {
  const { theme, toggleTheme } = useTheme();
  const [selectedSection, setSelectedSection] = useState<string>("7");
  const [hoveredParagraph, setHoveredParagraph] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [viewMode, setViewMode] = useState<ViewMode>("columns");
  
  // Refs for synchronized scrolling
  const adScrollRef = useRef<HTMLDivElement>(null);
  const jrScrollRef = useRef<HTMLDivElement>(null);
  const drScrollRef = useRef<HTMLDivElement>(null);
  const isScrollingRef = useRef<string | null>(null);

  const { data, isLoading, error } = trpc.affidavit.getData.useQuery();

  // Synchronized scroll handler
  const handleScroll = (source: 'ad' | 'jr' | 'dr') => {
    if (isScrollingRef.current && isScrollingRef.current !== source) return;
    
    isScrollingRef.current = source;
    
    const sourceRef = source === 'ad' ? adScrollRef : source === 'jr' ? jrScrollRef : drScrollRef;
    const sourceEl = sourceRef.current;
    if (!sourceEl) return;

    const scrollPercentage = sourceEl.scrollTop / (sourceEl.scrollHeight - sourceEl.clientHeight);
    
    // Sync other columns
    [adScrollRef, jrScrollRef, drScrollRef].forEach((ref, idx) => {
      const refName = ['ad', 'jr', 'dr'][idx];
      if (refName !== source && ref.current) {
        const targetScrollHeight = ref.current.scrollHeight - ref.current.clientHeight;
        ref.current.scrollTop = scrollPercentage * targetScrollHeight;
      }
    });

    setTimeout(() => {
      isScrollingRef.current = null;
    }, 50);
  };

  // Search functionality
  const searchResults = useMemo(() => {
    if (!data || !searchQuery.trim()) return [];
    
    const results: Array<{
      section: string;
      paragraph: string;
      type: 'AD' | 'JR' | 'DR';
      content: string;
      match: string;
    }> = [];

    Object.entries(data).forEach(([sectionNum, section]) => {
      // Search AD paragraphs
      Object.entries(section.paragraphs).forEach(([paraNum, paraData]) => {
        const content = typeof paraData === 'string' ? paraData : paraData.content;
        if (content.toLowerCase().includes(searchQuery.toLowerCase()) || 
            paraNum.toLowerCase().includes(searchQuery.toLowerCase())) {
          results.push({
            section: sectionNum,
            paragraph: paraNum,
            type: 'AD',
            content,
            match: searchQuery
          });
        }
      });

      // Search JR responses
      Object.entries(section.jr_responses || {}).forEach(([paraNum, paraData]) => {
        const content = typeof paraData === 'string' ? paraData : paraData.content;
        if (content.toLowerCase().includes(searchQuery.toLowerCase()) || 
            paraNum.toLowerCase().includes(searchQuery.toLowerCase())) {
          results.push({
            section: sectionNum,
            paragraph: paraNum,
            type: 'JR',
            content,
            match: searchQuery
          });
        }
      });

      // Search DR responses
      Object.entries(section.dr_responses || {}).forEach(([paraNum, paraData]) => {
        const content = typeof paraData === 'string' ? paraData : paraData.content;
        if (content.toLowerCase().includes(searchQuery.toLowerCase()) || 
            paraNum.toLowerCase().includes(searchQuery.toLowerCase())) {
          results.push({
            section: sectionNum,
            paragraph: paraNum,
            type: 'DR',
            content,
            match: searchQuery
          });
        }
      });
    });

    return results;
  }, [data, searchQuery]);

  const handleSearchResultClick = (section: string, paragraph: string, type: string) => {
    setSelectedSection(section);
    setSearchQuery("");
    setTimeout(() => {
      const element = document.getElementById(`${type.toLowerCase()}-${paragraph}`);
      element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
  };

  const exportPDF = () => {
    if (!data || !data[selectedSection]) return;

    const pdf = new jsPDF();
    const section = data[selectedSection];
    let yPos = 20;

    pdf.setFontSize(16);
    pdf.text(`Section ${selectedSection}: ${section.title}`, 20, yPos);
    yPos += 15;

    pdf.setFontSize(10);
    const adParagraphs = Object.keys(section.paragraphs).sort();

    adParagraphs.forEach((adNum) => {
      if (yPos > 270) {
        pdf.addPage();
        yPos = 20;
      }

      const adData = section.paragraphs[adNum];
      const adContent = typeof adData === 'string' ? adData : adData.content;
      
      pdf.setFont("helvetica", "bold");
      pdf.text(`AD ${adNum}`, 20, yPos);
      yPos += 7;

      pdf.setFont("helvetica", "normal");
      const adLines = pdf.splitTextToSize(adContent, 170);
      pdf.text(adLines, 20, yPos);
      yPos += adLines.length * 5 + 5;
    });

    pdf.save(`affidavit-comparison-section-${selectedSection}.pdf`);
    toast.success("PDF exported successfully!");
  };

  const isHighlighted = (paraNum: string) => {
    if (!hoveredParagraph) return false;
    const baseHovered = hoveredParagraph.split('.').slice(0, 2).join('.');
    const basePara = paraNum.split('.').slice(0, 2).join('.');
    return baseHovered === basePara;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <FileText className="h-12 w-12 animate-pulse mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Loading affidavit data...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <p className="text-destructive">Error loading affidavit data</p>
          <p className="text-sm text-muted-foreground mt-2">
            {error?.message || "Unknown error"}
          </p>
        </div>
      </div>
    );
  }

  const section = data[selectedSection];
  if (!section) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <p className="text-muted-foreground">Section {selectedSection} not found</p>
      </div>
    );
  }

  const adParagraphs = Object.keys(section.paragraphs).sort((a, b) => {
    const aParts = a.split('.').map(Number);
    const bParts = b.split('.').map(Number);
    for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
      if ((aParts[i] || 0) !== (bParts[i] || 0)) {
        return (aParts[i] || 0) - (bParts[i] || 0);
      }
    }
    return 0;
  });

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-6 w-6" />
            <div>
              <h1 className="text-lg font-semibold">Affidavit Comparison</h1>
              <p className="text-xs text-muted-foreground">AD Paragraphs 7-11 vs JR/DR Responses</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search paragraphs or keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 w-64"
              />
              {searchQuery && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7 p-0"
                  onClick={() => setSearchQuery("")}
                >
                  <X className="h-4 w-4" />
                </Button>
              )}
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center gap-1 border rounded-lg p-1">
              <Button
                variant={viewMode === "columns" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("columns")}
                className="h-8"
              >
                <Columns3 className="h-4 w-4 mr-1" />
                Columns
              </Button>
              <Button
                variant={viewMode === "grouped" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("grouped")}
                className="h-8"
              >
                <List className="h-4 w-4 mr-1" />
                Grouped
              </Button>
            </div>

            {/* Export PDF */}
            <Button variant="outline" size="sm" onClick={exportPDF}>
              <Download className="h-4 w-4 mr-2" />
              Export PDF
            </Button>

            {/* Theme Toggle */}
            <Button variant="outline" size="icon" onClick={toggleTheme}>
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        {/* Search Results */}
        {searchQuery && searchResults.length > 0 && (
          <div className="border-t bg-muted/50">
            <div className="container py-4">
              <p className="text-sm font-medium mb-2">
                Found {searchResults.length} result{searchResults.length !== 1 ? 's' : ''}
              </p>
              <ScrollArea className="h-32">
                <div className="space-y-2">
                  {searchResults.map((result, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2 p-2 rounded-lg hover:bg-background cursor-pointer"
                      onClick={() => handleSearchResultClick(result.section, result.paragraph, result.type)}
                    >
                      <Badge variant="secondary">Section {result.section}</Badge>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="outline" className="text-xs">
                            {result.type} {result.paragraph}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {result.content.substring(0, 150)}...
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </div>
          </div>
        )}
      </header>

      {/* Section Tabs */}
      <div className="border-b">
        <div className="container">
          <Tabs value={selectedSection} onValueChange={setSelectedSection} className="w-full">
            <TabsList className="w-full justify-start h-12 bg-transparent">
              {Object.keys(data).map((sectionNum) => (
                <TabsTrigger key={sectionNum} value={sectionNum} className="px-6">
                  Section {sectionNum}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
        </div>
      </div>

      {/* Main Content */}
      <main className="container py-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-2">
            Section {selectedSection}: {section.title}
          </h2>
          <div className="flex gap-2">
            <Badge variant="outline">{adParagraphs.length} AD Paragraphs</Badge>
            <Badge variant="outline">{Object.keys(section?.jr_responses || {}).length} JR Responses</Badge>
            <Badge variant="outline">{Object.keys(section?.dr_responses || {}).length} DR Responses</Badge>
          </div>
        </div>

        {viewMode === "columns" ? (
          /* Column View */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* AD Column */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Peter's AD Paragraphs</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <ScrollArea 
                  className="h-[calc(100vh-14rem)] lg:h-[calc(100vh-12rem)]"
                  onScrollCapture={() => handleScroll('ad')}
                >
                  <div className="space-y-4 p-6 pt-0" ref={adScrollRef}>
                    {adParagraphs.map((adNum) => {
                      const adData = section.paragraphs[adNum];
                      const content = typeof adData === 'string' ? adData : adData.content;
                      const severity = typeof adData === 'object' ? adData.severity : 5;
                      const summary = typeof adData === 'object' ? adData.summary : null;
                      const annexures = typeof adData === 'object' ? adData.annexures : [];

                      return (
                        <div 
                          key={adNum} 
                          id={`ad-${adNum}`} 
                          className={`group scroll-mt-20 transition-all duration-200 rounded-lg p-3 -mx-3 border ${
                            isHighlighted(adNum) 
                              ? 'ring-2 ring-primary/20' 
                              : ''
                          } ${getSeverityColor(severity || 5)}`}
                          onMouseEnter={() => setHoveredParagraph(adNum)}
                          onMouseLeave={() => setHoveredParagraph(null)}
                        >
                          <div className="flex items-start gap-2 mb-2">
                            <Badge className={`shrink-0 ${getSeverityBadgeColor(severity || 5)}`}>
                              AD {adNum}
                            </Badge>
                            <CommentDialog 
                              sectionNumber={selectedSection} 
                              paragraphNumber={adNum} 
                              paragraphType="AD" 
                            />
                          </div>
                          {summary && (
                            <p className="text-xs font-medium text-muted-foreground mb-2 italic">
                              {summary}
                            </p>
                          )}
                          <p className="text-sm leading-relaxed">{content}</p>
                          {annexures && annexures.length > 0 && (
                            <div className="mt-2 pt-2 border-t">
                              <p className="text-xs font-medium text-muted-foreground mb-1">Annexures:</p>
                              <div className="flex flex-wrap gap-1">
                                {annexures.map((annex, idx) => (
                                  <Badge key={idx} variant="outline" className="text-xs">
                                    {annex}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* JR Column */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Jacqueline's JR Responses</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <ScrollArea 
                  className="h-[calc(100vh-14rem)] lg:h-[calc(100vh-12rem)]"
                  onScrollCapture={() => handleScroll('jr')}
                >
                  <div className="space-y-4 p-6 pt-0" ref={jrScrollRef}>
                    {Object.keys(section.jr_responses || {})
                      .sort((a, b) => {
                        const aParts = a.split('.').map(Number);
                        const bParts = b.split('.').map(Number);
                        for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
                          if ((aParts[i] || 0) !== (bParts[i] || 0)) {
                            return (aParts[i] || 0) - (bParts[i] || 0);
                          }
                        }
                        return 0;
                      })
                      .map((jrNum) => {
                        const jrData = section.jr_responses?.[jrNum];
                        if (!jrData) return null;
                        
                        const content = typeof jrData === 'string' ? jrData : jrData.content;
                        const evidenceStrength = typeof jrData === 'object' ? jrData.evidenceStrength : 5;
                        const annexures = typeof jrData === 'object' ? jrData.annexures : [];

                        return (
                          <div 
                            key={jrNum} 
                            id={`jr-${jrNum}`} 
                            className={`group scroll-mt-20 transition-all duration-200 rounded-lg p-3 -mx-3 border ${
                              isHighlighted(jrNum) 
                                ? 'ring-2 ring-secondary/30' 
                                : ''
                            } ${getEvidenceColor(evidenceStrength || 5)}`}
                            onMouseEnter={() => setHoveredParagraph(jrNum)}
                            onMouseLeave={() => setHoveredParagraph(null)}
                          >
                            <div className="flex items-start gap-2 mb-2">
                              <Badge 
                                variant="secondary" 
                                className={`shrink-0 ${getEvidenceBadgeColor(evidenceStrength || 5)}`}
                              >
                                JR {jrNum}
                              </Badge>
                              <CommentDialog 
                                sectionNumber={selectedSection} 
                                paragraphNumber={jrNum} 
                                paragraphType="JR" 
                              />
                            </div>
                            <p className="text-sm leading-relaxed">{content}</p>
                            {annexures && annexures.length > 0 && (
                              <div className="mt-2 pt-2 border-t">
                                <p className="text-xs font-medium text-muted-foreground mb-1">Evidence:</p>
                                <div className="flex flex-wrap gap-1">
                                  {annexures.map((annex, idx) => (
                                    <Badge key={idx} variant="outline" className="text-xs">
                                      {annex}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* DR Column */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Daniel's DR Responses</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <ScrollArea 
                  className="h-[calc(100vh-14rem)] lg:h-[calc(100vh-12rem)]"
                  onScrollCapture={() => handleScroll('dr')}
                >
                  <div className="space-y-4 p-6 pt-0" ref={drScrollRef}>
                    {Object.keys(section.dr_responses || {})
                      .sort((a, b) => {
                        const aParts = a.split('.').map(Number);
                        const bParts = b.split('.').map(Number);
                        for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
                          if ((aParts[i] || 0) !== (bParts[i] || 0)) {
                            return (aParts[i] || 0) - (bParts[i] || 0);
                          }
                        }
                        return 0;
                      })
                      .map((drNum) => {
                        const drData = section.dr_responses?.[drNum];
                        if (!drData) return null;
                        
                        const content = typeof drData === 'string' ? drData : drData.content;
                        const evidenceStrength = typeof drData === 'object' ? drData.evidenceStrength : 5;
                        const annexures = typeof drData === 'object' ? drData.annexures : [];

                        return (
                          <div 
                            key={drNum} 
                            id={`dr-${drNum}`} 
                            className={`group scroll-mt-20 transition-all duration-200 rounded-lg p-3 -mx-3 border ${
                              isHighlighted(drNum) 
                                ? 'ring-2 ring-secondary/30' 
                                : ''
                            } ${getEvidenceColor(evidenceStrength || 5)}`}
                            onMouseEnter={() => setHoveredParagraph(drNum)}
                            onMouseLeave={() => setHoveredParagraph(null)}
                          >
                            <div className="flex items-start gap-2 mb-2">
                              <Badge 
                                variant="secondary" 
                                className={`shrink-0 ${getEvidenceBadgeColor(evidenceStrength || 5)}`}
                              >
                                DR {drNum}
                              </Badge>
                              <CommentDialog 
                                sectionNumber={selectedSection} 
                                paragraphNumber={drNum} 
                                paragraphType="DR" 
                              />
                            </div>
                            <p className="text-sm leading-relaxed">{content}</p>
                            {annexures && annexures.length > 0 && (
                              <div className="mt-2 pt-2 border-t">
                                <p className="text-xs font-medium text-muted-foreground mb-1">Evidence:</p>
                                <div className="flex flex-wrap gap-1">
                                  {annexures.map((annex, idx) => (
                                    <Badge key={idx} variant="outline" className="text-xs">
                                      {annex}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        ) : (
          /* Grouped View */
          <ScrollArea className="h-[calc(100vh-16rem)]">
            <div className="space-y-6">
              {adParagraphs.map((adNum) => {
                const adData = section.paragraphs[adNum];
                const adContent = typeof adData === 'string' ? adData : adData.content;
                const severity = typeof adData === 'object' ? adData.severity : 5;
                const summary = typeof adData === 'object' ? adData.summary : null;
                const adAnnexures = typeof adData === 'object' ? adData.annexures : [];

                // Find matching JR and DR responses
                const matchingJR = Object.entries(section.jr_responses || {})
                  .filter(([jrNum]) => jrNum.startsWith(adNum))
                  .sort(([a], [b]) => a.localeCompare(b));
                
                const matchingDR = Object.entries(section.dr_responses || {})
                  .filter(([drNum]) => drNum.startsWith(adNum))
                  .sort(([a], [b]) => a.localeCompare(b));

                return (
                  <Card key={adNum} className={`${getSeverityColor(severity || 5)} border-2`}>
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Badge className={`${getSeverityBadgeColor(severity || 5)}`}>
                              AD {adNum}
                            </Badge>
                            <CommentDialog 
                              sectionNumber={selectedSection} 
                              paragraphNumber={adNum} 
                              paragraphType="AD" 
                            />
                          </div>
                          {summary && (
                            <p className="text-sm font-medium text-muted-foreground italic mb-2">
                              {summary}
                            </p>
                          )}
                          <CardTitle className="text-base font-normal leading-relaxed">
                            {adContent}
                          </CardTitle>
                          {adAnnexures && adAnnexures.length > 0 && (
                            <div className="mt-3">
                              <p className="text-xs font-medium text-muted-foreground mb-1">Annexures:</p>
                              <div className="flex flex-wrap gap-1">
                                {adAnnexures.map((annex, idx) => (
                                  <Badge key={idx} variant="outline" className="text-xs">
                                    {annex}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {/* JR Responses */}
                      {matchingJR.length > 0 && (
                        <div className="space-y-3">
                          <h4 className="text-sm font-semibold text-secondary-foreground">
                            Jacqueline's Responses
                          </h4>
                          {matchingJR.map(([jrNum, jrData]) => {
                            const content = typeof jrData === 'string' ? jrData : jrData.content;
                            const evidenceStrength = typeof jrData === 'object' ? jrData.evidenceStrength : 5;
                            const annexures = typeof jrData === 'object' ? jrData.annexures : [];

                            return (
                              <div 
                                key={jrNum} 
                                className={`rounded-lg p-3 border ${getEvidenceColor(evidenceStrength || 5)}`}
                              >
                                <div className="flex items-start gap-2 mb-2">
                                  <Badge 
                                    variant="secondary" 
                                    className={`shrink-0 text-xs ${getEvidenceBadgeColor(evidenceStrength || 5)}`}
                                  >
                                    JR {jrNum}
                                  </Badge>
                                  <CommentDialog 
                                    sectionNumber={selectedSection} 
                                    paragraphNumber={jrNum} 
                                    paragraphType="JR" 
                                  />
                                </div>
                                <p className="text-sm leading-relaxed">{content}</p>
                                {annexures && annexures.length > 0 && (
                                  <div className="mt-2 pt-2 border-t">
                                    <p className="text-xs font-medium text-muted-foreground mb-1">Evidence:</p>
                                    <div className="flex flex-wrap gap-1">
                                      {annexures.map((annex, idx) => (
                                        <Badge key={idx} variant="outline" className="text-xs">
                                          {annex}
                                        </Badge>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {/* DR Responses */}
                      {matchingDR.length > 0 && (
                        <div className="space-y-3">
                          <h4 className="text-sm font-semibold text-secondary-foreground">
                            Daniel's Responses
                          </h4>
                          {matchingDR.map(([drNum, drData]) => {
                            const content = typeof drData === 'string' ? drData : drData.content;
                            const evidenceStrength = typeof drData === 'object' ? drData.evidenceStrength : 5;
                            const annexures = typeof drData === 'object' ? drData.annexures : [];

                            return (
                              <div 
                                key={drNum} 
                                className={`rounded-lg p-3 border ${getEvidenceColor(evidenceStrength || 5)}`}
                              >
                                <div className="flex items-start gap-2 mb-2">
                                  <Badge 
                                    variant="secondary" 
                                    className={`shrink-0 text-xs ${getEvidenceBadgeColor(evidenceStrength || 5)}`}
                                  >
                                    DR {drNum}
                                  </Badge>
                                  <CommentDialog 
                                    sectionNumber={selectedSection} 
                                    paragraphNumber={drNum} 
                                    paragraphType="DR" 
                                  />
                                </div>
                                <p className="text-sm leading-relaxed">{content}</p>
                                {annexures && annexures.length > 0 && (
                                  <div className="mt-2 pt-2 border-t">
                                    <p className="text-xs font-medium text-muted-foreground mb-1">Evidence:</p>
                                    <div className="flex flex-wrap gap-1">
                                      {annexures.map((annex, idx) => (
                                        <Badge key={idx} variant="outline" className="text-xs">
                                          {annex}
                                        </Badge>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </ScrollArea>
        )}
      </main>
    </div>
  );
}
