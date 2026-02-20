from database import Session, Alert
from datetime import datetime

class AlertEngine:
    def __init__(self):
        self.db = Session()
    
    def check_new_threat(self, threat):
        """Check if new threat matches any user alerts"""
        
        # Sample users (in real app, ye database se aayenge)
        users = [
            {
                "id": 1, 
                "email": "admin@hospital.com", 
                "industry": "Healthcare",
                "domains": ["hospital.com", "healthcare.org"]
            },
            {
                "id": 2, 
                "email": "security@bank.com", 
                "industry": "Finance",
                "domains": ["bank.com", "secure-bank.com"]
            }
        ]
        
        for user in users:
            # 1. Industry-based alert
            if user["industry"] and threat.tags:
                threat_tags = str(threat.tags).lower()
                if user["industry"].lower() in threat_tags:
                    self.create_alert(
                        user_id=user["id"],
                        threat_id=threat.id,
                        alert_type="industry",
                        message=f"New threat targeting {user['industry']} industry: {threat.indicator}"
                    )
                    print(f"📧 Industry Alert: {user['email']} - {threat.indicator}")
            
            # 2. Brand monitoring (domain match)
            for domain in user["domains"]:
                if domain in threat.indicator:
                    self.create_alert(
                        user_id=user["id"],
                        threat_id=threat.id,
                        alert_type="brand",
                        message=f"Your domain '{domain}' found in threat feed: {threat.indicator}"
                    )
                    print(f"🏢 Brand Alert: {user['email']} - {domain} found")
    
    def create_alert(self, user_id, threat_id, alert_type, message):
        """Save alert to database"""
        alert = Alert(
            user_id=user_id,
            threat_id=threat_id,
            alert_type=alert_type,
            message=message,
            status="new"
        )
        self.db.add(alert)
        self.db.commit()
        print(f"Alert saved: {message[:50]}...")
    
    def close(self):
        self.db.close()