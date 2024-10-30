import requests
import json

def test_health():
    """Test the health check endpoint"""
    response = requests.get('http://localhost:5000/health')
    print('\nHealth Check Response:')
    print(json.dumps(response.json(), indent=2))

def test_trigger_shortcut():
    """Test the shortcut trigger endpoint"""
    data = {
        'shortcutName': 'VoiceflowRecord'
    }
    response = requests.post(
        'http://localhost:5000/trigger-shortcut',
        json=data
    )
    print('\nTrigger Shortcut Response:')
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print("Running tests...")
    test_health()
    test_trigger_shortcut()