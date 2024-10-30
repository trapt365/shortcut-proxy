from flask import Flask, request, jsonify
from urllib.parse import quote
import logging
from datetime import datetime
import threading
import time
import requests

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/trigger-shortcut', methods=['POST'])
def trigger_shortcut():
    """Endpoint to trigger iOS shortcuts"""
    try:
        data = request.get_json()
        
        if not data or 'shortcutName' not in data:
            return jsonify({
                'success': False,
                'error': 'Shortcut name is required'
            }), 400
        
        shortcut_name = data['shortcutName']
        shortcut_url = f"shortcuts://run-shortcut?name={quote(shortcut_name)}"
        
        logger.info(f"Shortcut URL generated: {shortcut_url}")
        
        return jsonify({
            'success': True,
            'message': 'Shortcut triggered',
            'url': shortcut_url,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error triggering shortcut: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def run_server():
    """Run the Flask server"""
    app.run(port=5000, debug=False)

def run_tests():
    """Run test requests"""
    time.sleep(2)  # Wait for server to start
    
    print("\nRunning tests...")
    
    try:
        # Test health endpoint
        health_response = requests.get('http://localhost:5000/health')
        print("\nHealth Check Response:")
        print(health_response.json())

        # Test shortcut trigger
        data = {'shortcutName': 'VoiceflowRecord'}
        trigger_response = requests.post(
            'http://localhost:5000/trigger-shortcut',
            json=data
        )
        print("\nTrigger Shortcut Response:")
        print(trigger_response.json())
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure server is running on port 5000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == '__main__':
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run tests
    run_tests()
    
    # Keep main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")