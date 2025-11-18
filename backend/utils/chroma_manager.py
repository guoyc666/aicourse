import os
import chromadb
from .ai_client import get_embedding


class VectorStore:
    """嵌入式 Chroma 向量数据库"""

    def __init__(
        self,
        chroma_dir=os.getenv("CHROMA_DB_DIR"),
        collection_name=os.getenv("CHROMA_COLLECTION"),
    ):
        self.client = chromadb.PersistentClient(path=chroma_dir)
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)

    def insert(self, documents, metadatas, ids):
        embeddings = get_embedding(documents)
        embeddings = [e.embedding for e in embeddings]
        self.collection.add(
            documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings
        )

    def query(self, query: str, top_k: int = 10):
        query_vector = get_embedding(query)
        query_vector = query_vector[0].embedding
        return self.collection.query(query_embeddings=query_vector, n_results=top_k)

    def count(self):
        return self.collection.count()


if __name__ == "__main__":
    vs = VectorStore(chroma_dir="./chroma_db", collection_name="test_collection")
    vs.insert(
        documents=["今天天气真好！", "我喜欢学习编程。", "人工智能是未来的趋势。"],
        metadatas=[{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}],
        ids=["doc_1", "doc_2", "doc_3"],
    )
    print("向量数量：", vs.count())

    results = vs.query("什么是人工智能？", top_k=2)
    for doc, meta, id in zip(
        results["documents"][0], results["metadatas"][0], results["ids"][0]
    ):
        print(f"ID: {id}, Meta: {meta}, Doc: {doc}")
