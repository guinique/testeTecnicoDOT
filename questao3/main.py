import os
os.environ["USE_TF"] = "NO"
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langfuse import observe
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

class SemanticSearchSystem:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    @observe()
    def load_and_chunk_pdfs(self, folder_path, chunk_size=500, chunk_overlap=50):
        # recursive character splitter to keep sentences and paragraphs together
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        raw_chunks = []
        
        # Procura os arquivos na pasta docs
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                reader = PdfReader(file_path)
                
                full_text = ""
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        full_text += extracted_text + "\n"
                        
                # separa os chunks do texto completo do PDF
                if full_text.strip():
                    chunks = text_splitter.split_text(full_text)
                    raw_chunks.extend(chunks)
                    
        return raw_chunks

    @observe()
    def index_documents(self, documents):
        if not documents:
            raise ValueError("No documents provided to index.")

        self.documents = documents
        
        embeddings = self.model.encode(documents)
        embeddings = np.array(embeddings).astype('float32')
        
        vector_dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(vector_dimension)
        self.index.add(embeddings)

    @observe()
    def search(self, query, top_k=5):
        if not self.index:
            raise ValueError("The index is empty. Please index documents first.")

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "document": self.documents[idx],
                "distance": distances[0][i]
            })
            
        return results

if __name__ == "__main__":
    search_system = SemanticSearchSystem()
    
    # caminho para a pasta onde os PDFs estão localizados
    docs_folder = "docs"
    
    print(f"Reading and chunking PDFs from '{docs_folder}' directory...")
    document_chunks = search_system.load_and_chunk_pdfs(
        folder_path=docs_folder, 
        chunk_size=500, 
        chunk_overlap=50
    )
    
    print(f"Total document chunks created: {len(document_chunks)}")
    
    if document_chunks:
        print("Indexing documents into FAISS...")
        search_system.index_documents(document_chunks)

        # queries para testar o sistema, sem chatbot
        queries = [
            "What is bone age?",
            "how bonexpert works?"
        ]

        for query in queries:
            print(f"\nQuery: '{query}'")
            results = search_system.search(query, top_k=2)
            
            for res in results:
                print(f"Distance: {res['distance']:.4f}")
                # limit the output string size so it does not flood the terminal
                print(f"Result: {res['document'][:200]}...\n")
    else:
        print("No text could be extracted. Make sure there are readable PDFs in the docs folder.")