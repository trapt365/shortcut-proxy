from flask import Flask, request, jsonify
from urllib.parse import quote
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Shortcut proxy server is running',
        'timestamp': datetime.now().isoformat()
    })

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)