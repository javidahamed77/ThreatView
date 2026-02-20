from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime, timedelta
from database import Session
from models import ThreatIndicator

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.db = Session()
    
    def generate_weekly_report(self):
        """Generate Weekly Threat Landscape PDF"""
        
        # Filename with date
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"ThreatView_Weekly_Report_{date_str}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title_style = self.styles['Heading1']
        title = Paragraph("ThreatView Weekly Threat Landscape Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Date
        date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(date_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        summary_data = self.get_summary_stats()
        summary_text = f"""
        Total Threats Detected: {summary_data['total']}
        Critical/High Severity: {summary_data['critical_high']}
        New Threats (24h): {summary_data['last_24h']}
        Top Attack Vector: Phishing
        """
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Top Threats Table
        story.append(Paragraph("Top Threats This Week", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        threats = self.get_top_threats()
        table_data = [['Indicator', 'Type', 'Severity', 'Source']]
        
        for t in threats:
            table_data.append([
                t.indicator[:30] + '...' if len(t.indicator) > 30 else t.indicator,
                t.type.upper(),
                t.severity.upper(),
                t.source
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        
        # Build PDF
        doc.build(story)
        self.db.close()
        
        print(f"PDF Generated: {filename}")
        return filename
    
    def get_summary_stats(self):
        week_ago = datetime.now() - timedelta(days=7)
        day_ago = datetime.now() - timedelta(days=1)
        
        total = self.db.query(ThreatIndicator).filter(
            ThreatIndicator.first_seen >= week_ago
        ).count()
        
        critical_high = self.db.query(ThreatIndicator).filter(
            ThreatIndicator.first_seen >= week_ago,
            ThreatIndicator.severity.in_(['critical', 'high'])
        ).count()
        
        last_24h = self.db.query(ThreatIndicator).filter(
            ThreatIndicator.first_seen >= day_ago
        ).count()
        
        return {
            'total': total,
            'critical_high': critical_high,
            'last_24h': last_24h
        }
    
    def get_top_threats(self, limit=10):
        week_ago = datetime.now() - timedelta(days=7)
        return self.db.query(ThreatIndicator).filter(
            ThreatIndicator.first_seen >= week_ago
        ).order_by(
            ThreatIndicator.severity.desc()
        ).limit(limit).all()

# Test
if __name__ == "__main__":
    gen = PDFReportGenerator()
    filename = gen.generate_weekly_report()
    print(f"Report saved: {filename}")