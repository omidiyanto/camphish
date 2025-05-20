from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import base64
import time
from datetime import datetime
import ssl

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        # Get the image data from the request
        image_data = request.json.get('image')
        
        # Remove the base64 prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode the base64 image
        image_binary = base64.b64decode(image_data)
        
        # Create a unique filename using timestamp
        filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the image to the uploads folder
        with open(filepath, 'wb') as f:
            f.write(image_binary)
        
        return jsonify({'success': True, 'message': 'Image captured successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # SSL context for HTTPS
    ssl_context = ('ssl/cert.pem', 'ssl/key.pem')
    
    # Run with HTTPS
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
