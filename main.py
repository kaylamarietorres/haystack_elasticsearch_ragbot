from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor, BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import clean_wiki_text, launch_es, convert_files_to_docs

# Launch Elasticsearch
launch_es()

# Initialize the DocumentStore with HTTPS, CA certificate, and authentication
document_store = ElasticsearchDocumentStore(
    host="localhost",
    username="elastic",  # Username (as used in the curl command)
    password="password",  # Password (ensure this is set correctly)
    scheme="https",  # Use "https" instead of "http"
    port=9200,
    verify_certs=True,  # Enable SSL certificate verification
    ca_certs="http_ca.crt",  # Path to your CA certificate
    index="document"
)

# Initialize the PDFToTextConverter
converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])

# Initialize the PreProcessor
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=200,
    split_respect_sentence_boundary=True,
)

# Convert PDF files to text
pdf_file_paths = ["data/ElasticsearchPDF.pdf"]  # Update with your PDF file paths
documents = []

for path in pdf_file_paths:
    converted = converter.convert(file_path=path, meta=None)[0]
    processed = preprocessor.process(converted)
    documents.extend(processed)

# Write documents to the DocumentStore
document_store.write_documents(documents)

# Initialize the Retriever
retriever = BM25Retriever(document_store=document_store)

# Initialize the DocumentSearchPipeline
pipeline = DocumentSearchPipeline(retriever=retriever)

# Search for a query
query = "index"
result = pipeline.run(query=query)
print(result)
