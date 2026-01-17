from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
from crossword_solver import CrosswordSolver

app = Flask(__name__, static_folder='.')
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the crossword solver
solver = CrosswordSolver()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        pattern = data.get('pattern', '')
        known_letters = data.get('known_letters', '')
        length = data.get('length')

        logger.info(f"Search request - Pattern: {pattern}, Known letters: {known_letters}, Length: {length}")

        # Search for matching words
        results = solver.find_matches(pattern, known_letters, length)

        return jsonify({
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        logger.error(f"Error processing search: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
