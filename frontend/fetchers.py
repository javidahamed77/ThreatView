import requests
import os
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# API key - paste your actual key here
OTX_API_KEY = "65065c46582d67b7adffc2ac614fa71ab44f12ae2af8efbd9ee4f8157b2ea272"

def fetch_alienvault():
    """Fetch threat data from AlienVault OTX"""
    
    if not OTX_API_KEY:
        print("No AlienVault API key found")
        return []
    
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    
    try:
        print("Fetching AlienVault OTX...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            pulses = data.get("results", [])
            print(f"Found {len(pulses)} pulses")
            return pulses
        elif response.status_code == 403:
            print("Error 403: API key invalid or expired")
            print("Please regenerate your API key at https://otx.alienvault.com")
        elif response.status_code == 429:
            print("Error 429: Rate limit exceeded. Wait a few minutes.")
        else:
            print(f"Error {response.status_code}: {response.text[:100]}")
            
    except requests.exceptions.ConnectionError:
        print("Connection error: Check your internet")
    except Exception as e:
        print(f"Error: {e}")
    
    return []

def fetch_phishtank():
    """Fetch phishing URLs from PhishTank"""
    
    url = "http://data.phishtank.com/data/online-valid.json"
    
    try:
        print("Fetching PhishTank...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} phishing URLs")
            return data
        elif response.status_code == 429:
            print("PhishTank rate limit exceeded. Wait a few minutes.")
        else:
            print(f"PhishTank error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("PhishTank timeout - server slow")
    except requests.exceptions.ConnectionError:
        print("Connection error: Check your internet")
    except Exception as e:
        print(f"Error: {e}")
    
    return []

def test_alienvault_key():
    """Test if API key is working"""
    
    if not OTX_API_KEY:
        print("No API key set")
        return False
    
    url = "https://otx.alienvault.com/api/v1/user/profile"
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("API key is valid")
            return True
        else:
            print(f"API key invalid (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"Error testing key: {e}")
        return False

# For testing
if __name__ == "__main__":
    print("Testing AlienVault API key...")
    test_alienvault_key()
    
    print("\nFetching AlienVault data...")
    pulses = fetch_alienvault()
    print(f"Got {len(pulses)} pulses")
    
    print("\nFetching PhishTank data...")
    entries = fetch_phishtank()
    print(f"Got {len(entries)} entries")