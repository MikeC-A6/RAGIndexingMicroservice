import os
import json
from src.main import create_app
from src.preprocessing import PreprocessingModule

def run_pdf_chunking():
    # Initialize the app and preprocessing
    app = create_app()
    preprocessor = PreprocessingModule()

    # Setup paths
    test_docs_dir = "test_docs"
    test_pdf_path = os.path.join(test_docs_dir, "Test_PDF1.pdf")

    if not os.path.exists(test_pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {test_pdf_path}")

    # Configure document for processing
    test_data = {
        "documents": [{
            "type": "pdf",
            "content": "",
            "metadata": {
                "file_path": test_pdf_path,
                "source": test_pdf_path,
                "document_type": "pdf_document"
            }
        }],
        "indexing_strategy": "sentence_chunker",
        "chunk_params": {
            "max_sentences_per_chunk": 3,
            "min_sentence_length": 10,
            "overlap_sentences": 1
        }
    }

    # First preprocess the PDF
    processed_docs = preprocessor.process(test_data["documents"])

    # Now use the app client to chunk the processed content
    client = app.test_client()

    # Update the test data with processed content
    test_data["documents"] = processed_docs

    print("\nProcessing Configuration:")
    print(f"PDF Path: {test_pdf_path}")
    print(f"Strategy: {test_data['indexing_strategy']}")
    print(f"Chunk Parameters: {json.dumps(test_data['chunk_params'], indent=2)}")

    # Make the request
    response = client.post('/api/ingest', 
                          json=test_data,
                          headers={'Content-Type': 'application/json'})

    print("\nResponse Status:", response.status_code)

    if response.status_code == 200:
        result = response.get_json()

        # Save results
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "pdf_chunks.json")

        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\nResults saved to: {output_file}")
        print(f"\nNumber of chunks: {len(result)}")

        # Print first chunk as sample
        if result:
            print("\nSample chunk:")
            print(json.dumps(result[0], indent=2))
    else:
        print("Error:", response.get_json())

if __name__ == "__main__":
    run_pdf_chunking()