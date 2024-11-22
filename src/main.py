from flask import Flask, request, jsonify
from .chunking.manager import ChunkerManager
from .chunking.sentence_chunker import SentenceChunker
from .indexing.strategies import SimpleDirectoryReader

def create_app():
    app = Flask(__name__)

    # Initialize and register chunking strategies
    chunker_manager = ChunkerManager()
    # Changed this line - we pass the class, not an instance
    chunker_manager.register_strategy(SentenceChunker)  # Remove the parentheses

    @app.route('/api/ingest', methods=['POST'])
    def ingest():
        try:
            data = request.get_json()
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
