# Indexing Microservice for RAG Pipeline

This microservice is responsible for processing raw documents and generating structured output for the RAG (Retrieval-Augmented Generation) pipeline. It handles document preprocessing, applies various indexing strategies, and formats output for downstream embedding services.

## Architecture Overview

The service is organized into four main components:

1. API Gateway
   - Handles incoming requests
   - Manages request validation and routing
   - Exposes endpoints for document ingestion and strategy listing

2. Indexing Strategy Manager
   - Manages different indexing strategies
   - Supports extensible indexing modules
   - Currently supports SimpleDirectoryReader and JSON indexing

3. Preprocessing Module
   - Handles document cleaning and text extraction
   - Supports various document formats (Text, PDF)
   - Manages document chunking

4. Output Formatter
   - Standardizes output format
   - Ensures compatibility with the Embedding Service

## Project Structure

