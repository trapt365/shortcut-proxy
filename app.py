from flask import Flask, request, jsonify
from urllib.parse import quote
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/trigger-shortcut', methods=['POST'])
def trigger_shortcut():
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
        
        # Return HTML response with clickable link
        html_response = f"""
        <html>
            <body>
                <h2>Click to start recording:</h2>
                <a href="{shortcut_url}" style="
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007AFF;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-family: -apple-system, system-ui;
                    font-size: 16px;
                ">Start Recording</a>
            </body>
        </html>
        """
        
        return html_response, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        logger.error(f"Error triggering shortcut: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)