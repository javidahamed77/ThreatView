from models import ThreatIndicator
from datetime import datetime

class AlienVaultNormalizer:
    @staticmethod
    def normalize(pulse):
        threats = []
        for indicator in pulse.get('indicators', []):
            threat = ThreatIndicator(
                indicator=indicator.get('indicator', ''),
                type=indicator.get('type', '').lower(),
                source='alienvault',
                confidence=indicator.get('confidence', 50),
                severity=indicator.get('severity', 'medium'),
                tags=pulse.get('tags', []),
                description=pulse.get('description', '')[:200],
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                raw_data=indicator
            )
            threats.append(threat)
        return threats

class PhishTankNormalizer:
    @staticmethod
    def normalize(entry):
        threat = ThreatIndicator(
            indicator=entry.get('url', ''),
            type='url',
            source='phishtank',
            confidence=100 if entry.get('verified') else 50,
            severity='high' if entry.get('verified') else 'medium',
            tags=['phishing'],
            description=f"Phishing: {entry.get('target', 'unknown')}",
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            raw_data=entry
        )
        return [threat]