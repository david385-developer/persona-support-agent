from src.knowledge_base import KnowledgeBase

def main():
    print("=" * 50)
    print("  CloudFlow Knowledge Base Ingestion")
    print("=" * 50)
    print()

    kb = KnowledgeBase()
    documents = kb.load_documents()
    chunks = kb.chunk_documents(documents)
    kb.build_vector_store(chunks)

    print()
    print(f"Ingestion complete:")
    print(f"  Documents loaded: {len(documents)}")
    print(f"  Chunks created:   {len(chunks)}")
    print(f"  Vector store:     .vector_store/")
    print()
    print("You can now run: python cli.py")


if __name__ == "__main__":
    main()