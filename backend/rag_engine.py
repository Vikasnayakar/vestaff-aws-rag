from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_ollama import OllamaLLM


class RAGEngine:

    def __init__(self):

        # Embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = None


        # Prompt
        self.template = """
You are an AI assistant for AWS Customer Agreement.

Answer only using the provided context.

If the answer is not available in the context, reply exactly:

"I am sorry, but the answer to your question is not present in the provided document."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""


        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=[
                "context",
                "question"
            ]
        )


        # Local LLM
        self.llm = OllamaLLM(
            model="llama3.2:3b",
            temperature=0
            num_predict=150
        )

    def ingest_document(self, file_path: str) -> int:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )

        chunks = splitter.split_text(text)


        self.vector_store = FAISS.from_texts(
            chunks,
            self.embeddings
        )


        return len(chunks)


    def query(self, user_query: str):

        if self.vector_store is None:
            raise ValueError(
                "Document not ingested"
            )


        # Retrieve relevant chunks
        docs = self.vector_store.similarity_search(
            user_query,
            k=1
        )


        context = "\n\n---\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )



        chain = self.prompt | self.llm



        answer = chain.invoke(
            {
                "context": context,
                "question": user_query
            }
        )



        return {

            "answer": str(answer),

            "sources": [
                doc.page_content
                for doc in docs
            ]

        }