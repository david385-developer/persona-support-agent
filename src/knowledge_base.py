"""
Knowledge Base Module

Handles document loading, chunking, embedding, and vector search.
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from .config import config


def get_embeddings():
    """Create the embedding model. Runs locally, no API cost."""
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


class KnowledgeBase:
    """
    Manages the entire knowledge base lifecycle:
    load documents → chunk → embed → store in FAISS → retrieve
    """

    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = None
        self.documents = []

    def load_documents(self) -> List[Document]:
        """Load all documents from the data directory."""
        data_dir = config.DATA_DIR
        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        documents = []

        # Load .md files using TextLoader
        md_files = list(data_dir.glob("**/*.md"))
        for md_path in md_files:
            loader = TextLoader(str(md_path), encoding="utf-8")
            documents.extend(loader.load())

        # Load .txt files
        txt_files = list(data_dir.glob("**/*.txt"))
        for txt_path in txt_files:
            loader = TextLoader(str(txt_path), encoding="utf-8")
            documents.extend(loader.load())

        # Load .pdf files
        pdf_files = list(data_dir.glob("**/*.pdf"))
        for pdf_path in pdf_files:
            loader = PyPDFLoader(str(pdf_path))
            documents.extend(loader.load())

        # Add metadata
        for doc in documents:
            source = Path(doc.metadata.get("source", "unknown"))
            doc.metadata["source_file"] = source.name
            doc.metadata["section"] = self._extract_section(doc.page_content)

        self.documents = documents
        print(f"  Loaded {len(documents)} document(s) from {data_dir}")
        return documents

    def chunk_documents(self, documents: List[Document] = None) -> List[Document]:
        """Split documents into chunks for embedding."""
        docs = documents or self.documents
        if not docs:
            raise ValueError("No documents to chunk. Call load_documents() first.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
        )

        chunks = splitter.split_documents(docs)
        print(f"  Created {len(chunks)} chunk(s) from {len(docs)} document(s)")
        return chunks

    def build_vector_store(self, chunks: List[Document] = None) -> FAISS:
        """Build or load FAISS vector store."""
        store_path = config.VECTOR_STORE_DIR

        if store_path.exists() and any(store_path.iterdir()):
            try:
                self.vector_store = FAISS.load_local(
                    str(store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                print(f"  Loaded existing vector store from {store_path}")
                return self.vector_store
            except Exception as e:
                print(f"  Could not load existing store ({e}), rebuilding...")

        if chunks is None:
            documents = self.load_documents()
            chunks = self.chunk_documents(documents)

        self.vector_store = FAISS.from_documents(chunks, self.embeddings)

        store_path.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(store_path))
        print(f"  Built and saved vector store to {store_path}")
        return self.vector_store

    def retrieve(self, query: str, k: int = None) -> List[dict]:
        """
        Search the knowledge base for chunks relevant to the query.
        Returns scores normalized to 0-1 range using cosine similarity.
        """
        if self.vector_store is None:
            self.build_vector_store()

        k = k or config.TOP_K

        # Use similarity_search_with_score (raw scores)
        raw_results = self.vector_store.similarity_search_with_score(query, k=k)

        retrieved = []
        for doc, raw_score in raw_results:
            # Convert raw FAISS score to 0-1 similarity
            # FAISS uses L2 distance: lower = more similar
            # Convert: similarity = 1 / (1 + distance)
            similarity = float(1.0 / (1.0 + raw_score))

            # Clamp to 0-1 range
            similarity = max(0.0, min(1.0, similarity))

            retrieved.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source_file", "unknown"),
                "section": doc.metadata.get("section", ""),
                "page": doc.metadata.get("page", None),
                "score": round(similarity, 4),
            })

        return retrieved

    @staticmethod
    def _extract_section(content: str) -> str:
        """Extract the first heading from document content."""
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
        return "General"