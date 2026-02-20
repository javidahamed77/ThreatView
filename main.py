from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from database import Session
from models import ThreatIndicator, Alert
from datetime import datetime, timedelta
import csv
from io import StringIO
from report_generator import PDFReportGenerator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ThreatView API"}

@app.get("/api/stats")
def get_stats():
    db = Session()
    total = db.query(ThreatIndicator).count()
    last_24h = db.query(ThreatIndicator).filter(
        ThreatIndicator.last_seen >= datetime.now() - timedelta(hours=24)
    ).count()
    db.close()
    return {"total": total, "last_24h": last_24h}

@app.get("/api/threats")
def get_threats():
    db = Session()
    threats = db.query(ThreatIndicator).order_by(ThreatIndicator.last_seen.desc()).limit(100).all()
    db.close()
    return [
        {
            "id": t.id,
            "indicator": t.indicator,
            "type": t.type,
            "source": t.source,
            "severity": t.severity,
            "confidence": t.confidence,
            "last_seen": t.last_seen.isoformat() if t.last_seen else None
        }
        for t in threats
    ]

@app.get("/api/search")
def search_ioc(query: str):
    db = Session()
    results = db.query(ThreatIndicator).filter(
        ThreatIndicator.indicator.contains(query)
    ).all()
    db.close()
    
    return {
        "query": query,
        "found": len(results) > 0,
        "results": [
            {
                "indicator": r.indicator,
                "type": r.type,
                "source": r.source,
                "severity": r.severity,
                "confidence": r.confidence,
                "first_seen": r.first_seen.isoformat() if r.first_seen else None
            }
            for r in results
        ]
    }

@app.get("/api/alerts")
def get_alerts():
    db = Session()
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(20).all()
    db.close()
    
    return [
        {
            "id": a.id,
            "type": a.alert_type,
            "message": a.message,
            "status": a.status,
            "created_at": a.created_at.isoformat()
        }
        for a in alerts
    ]

@app.get("/api/reports/weekly")
async def generate_weekly_report():
    generator = PDFReportGenerator()
    filename = generator.generate_weekly_report()
    
    return FileResponse(
        filename, 
        media_type='application/pdf',
        filename=f"weekly_threat_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    )

@app.get("/api/threats/export")
async def export_threats_csv():
    db = Session()
    threats = db.query(ThreatIndicator).order_by(ThreatIndicator.last_seen.desc()).limit(1000).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Indicator', 'Type', 'Source', 'Severity', 'Confidence', 'First Seen'])
    
    for t in threats:
        writer.writerow([
            t.indicator,
            t.type,
            t.source,
            t.severity,
            t.confidence,
            t.first_seen.strftime('%Y-%m-%d')
        ])
    
    db.close()
    
    response = StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=threats_export.csv"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)