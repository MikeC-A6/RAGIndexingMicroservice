import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from .chunking.manager import ChunkerManager
from .chunking.sentence_chunker import SentenceChunker
from .indexing.strategies import SimpleDirectoryReader

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('src.config.ProductionConfig')
    
    # Initialize CORS
    CORS(app)
    
    # Register error handlers
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error="Method not allowed. This endpoint only accepts POST requests."), 405
        
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad request. Please ensure you're sending valid JSON data."), 400
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="Internal server error occurred."), 500
    
    # Configure logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask application startup')

    # Initialize and register chunking strategies
    chunker_manager = ChunkerManager()
    # Changed this line - we pass the class, not an instance
    chunker_manager.register_strategy(SentenceChunker)  # Remove the parentheses

    @app.route('/')
    def index():
        return jsonify({
            'status': 'online',
            'endpoints': {
                '/api/ingest': 'POST - Ingest and process documents',
                '/health': 'GET - Health check endpoint'
            }
        })

    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'indexing-microservice'
        })

    @app.route('/api/ingest', methods=['POST'])
    def ingest():
        try:
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
                
            try:
                data = request.get_json(force=True)
            except Exception as e:
                return jsonify({'error': 'Invalid JSON format'}), 400
            documents = data.get('documents', [])
            strategy_name = data.get('indexing_strategy')
            chunk_params = data.get('chunk_params')

            print("\nIncoming documents:", documents)  # Debug print

            if not documents:
                return jsonify({'error': 'No documents provided'}), 400

            # Process documents using the specified strategy
            if strategy_name == 'sentence_chunker':
                chunker = chunker_manager.get_strategy(strategy_name)
                processed_docs = chunker.chunk_document(
                    documents[0].get('content', ''),
                    documents[0].get('metadata', {}),
                    chunk_params
                )
                return jsonify(processed_docs)
            elif strategy_name == 'simple_directory':
                reader = SimpleDirectoryReader()
                result = reader.index(documents)
                return jsonify(result)

            return jsonify({'error': f'Unknown strategy: {strategy_name}'}), 400

        except Exception as e:
            print(f"\nError during processing: {str(e)}")  # Debug print
            return jsonify({'error': str(e)}), 500

    return app
