from flask import Flask
from .api.routes import api_bp
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': 'Indexing Microservice API',
            'endpoints': [
                '/api/ingest',
                '/api/list-strategies'
            ]
        }

    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error'}, 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
