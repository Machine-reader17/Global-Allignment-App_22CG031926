"""
BioSeqAligner - Backend Flask Application
Global and Local Sequence Alignment Tool
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.dirname(__file__))
from alignment import AlignmentTool

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

@app.route('/')
def index():
    """Serve the frontend index.html"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/align', methods=['POST'])
def align_sequences():
    """Endpoint: Perform sequence alignment"""
    try:
        data = request.json
        seq1 = data.get('seq1', '').upper().strip()
        seq2 = data.get('seq2', '').upper().strip()
        match = int(data.get('match', 2))
        mismatch = int(data.get('mismatch', -1))
        gap = int(data.get('gap', -2))
        alignment_type = data.get('type', 'global') # 'global' or 'local'
        
        if not seq1 or not seq2:
            return jsonify({'error': 'Two sequences are required'}), 400
            
        tool = AlignmentTool()
        
        if alignment_type == 'global':
            result = tool.global_alignment(seq1, seq2, match, mismatch, gap)
        else:
            result = tool.local_alignment(seq1, seq2, match, mismatch, gap)
            
        # Add original sequences for frontend reference
        result['seq1_orig'] = seq1
        result['seq2_orig'] = seq2
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'BioSeqAligner API'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"BioSeqAligner API running on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
