import streamlit as st
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor, BM25Retriever
from haystack.pipelines import DocumentSearchPipeline
import os
import tempfile
import time


# Retry logic to handle initial connection delay
def create_document_store():
    retries = 5
    for i in range(retries):
        try:
            document_store = ElasticsearchDocumentStore(
                host="elasticsearch",
                username="elastic",
                password=os.getenv("ELASTIC_PASSWORD"),
                scheme="http",  # Use 'http' scheme
                port=9200,
                verify_certs=False,  # Disable certificate verification
                index="document"
            )
            return document_store
        except Exception as e:
            st.error(f"Attempt {i + 1} - Failed to connect to Elasticsearch: {e}")
            time.sleep(10)
    raise ConnectionError("Failed to connect to Elasticsearch after multiple attempts.")


# Initialize the DocumentStore
document_store = create_document_store()

# Initialize the PDFToTextConverter and PreProcessor
converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=200,
    split_respect_sentence_boundary=True,
)

# Initialize the Retriever
retriever = BM25Retriever(document_store=document_store)
pipeline = DocumentSearchPipeline(retriever=retriever)

# Streamlit App
st.title("PDF Search Application")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Process PDF"):
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Convert PDF to text and process it
        with st.spinner('Processing...'):
            converted = converter.convert(file_path=temp_file_path, meta=None)[0]
            processed = preprocessor.process(converted)
            document_store.write_documents(processed)

        st.success("PDF processed and indexed successfully!")

        # Clean up the temporary file
        os.remove(temp_file_path)

search_query = st.text_input("Enter a search query")
if st.button("Search"):
    if search_query:
        # Perform the search query
        with st.spinner('Searching...'):
            result = pipeline.run(query=search_query)
            documents = result['documents']

            st.write("Search Results:")
            for doc in documents:
                st.markdown(f"**Document ID:** {doc.id}")
                formatted_content = doc.content.replace("\n", "<br>").replace("  ", "&nbsp;")
                st.markdown(formatted_content, unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.warning("Please enter a search query")