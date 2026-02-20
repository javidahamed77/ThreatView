import schedule
import time
from database import Session
from models import ThreatIndicator
from fetchers import fetch_alienvault, fetch_phishtank
from normalizers import AlienVaultNormalizer, PhishTankNormalizer
from alert_engine import AlertEngine
from datetime import datetime

def job_alienvault():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Fetching AlienVault...")
    pulses = fetch_alienvault()
    
    if not pulses:
        print("No pulses received from AlienVault")
        return
    
    db = Session()
    alert_engine = AlertEngine()
    count = 0
    
    try:
        for pulse in pulses:
            threats = AlienVaultNormalizer.normalize(pulse)
            for threat in threats:
                # Check if already exists
                existing = db.query(ThreatIndicator).filter_by(
                    indicator=threat.indicator, 
                    source='alienvault'
                ).first()
                
                if not existing:
                    db.add(threat)
                    db.flush()  # Get ID for alert engine
                    alert_engine.check_new_threat(threat)
                    count += 1
                    print(f"  + New threat: {threat.indicator[:50]}...")
        
        db.commit()
        print(f"Added {count} new AlienVault threats")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        alert_engine.close()
        db.close()

def job_phishtank():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Fetching PhishTank...")
    entries = fetch_phishtank()
    
    if not entries:
        print("No entries received from PhishTank")
        return
    
    db = Session()
    alert_engine = AlertEngine()
    count = 0
    
    try:
        for entry in entries[:20]:  # Limit to 20 entries
            threats = PhishTankNormalizer.normalize(entry)
            for threat in threats:
                existing = db.query(ThreatIndicator).filter_by(
                    indicator=threat.indicator,
                    source='phishtank'
                ).first()
                
                if not existing:
                    db.add(threat)
                    db.flush()
                    alert_engine.check_new_threat(threat)
                    count += 1
        
        db.commit()
        print(f"Added {count} new PhishTank threats")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        alert_engine.close()
        db.close()

# Schedule jobs
schedule.every(10).minutes.do(job_alienvault)   # Every 10 minutes
schedule.every(15).minutes.do(job_phishtank)    # Every 15 minutes

if __name__ == "__main__":
    print("ThreatView Scheduler Started")
    print("Jobs: AlienVault (10 min), PhishTank (15 min)")
    
    # Run once immediately
    job_alienvault()
    job_phishtank()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)