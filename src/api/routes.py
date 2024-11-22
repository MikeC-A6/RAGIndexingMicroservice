from flask import Blueprint, request, jsonify
from src.indexing.strategy_manager import StrategyManager
from src.preprocessing.processor import PreprocessingModule
from src.output.formatter import OutputFormatter

api_bp = Blueprint('api', __name__)

@api_bp.route('/ingest', methods=['POST'])
def ingest():
    """Handle document ingestion requests."""
    data = request.get_json()
    
    # Validate request
    if not data or 'documents' not in data or 'indexing_strategy' not in data:
        return jsonify({'error': 'Invalid request parameters'}), 400
    
    try:
        # Initialize components
        preprocessor = PreprocessingModule()
        strategy_manager = StrategyManager()
        output_formatter = OutputFormatter()
        
        # Process documents
        preprocessed_docs = preprocessor.process(data['documents'])
        indexed_data = strategy_manager.apply_strategy(
            data['indexing_strategy'],
            preprocessed_docs
        )
        formatted_output = output_formatter.format(indexed_data)
        
        return jsonify(formatted_output)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/list-strategies', methods=['GET'])
def list_strategies():
    """List available indexing strategies."""
    strategy_manager = StrategyManager()
    available_strategies = strategy_manager.get_available_strategies()
    return jsonify(available_strategies)
