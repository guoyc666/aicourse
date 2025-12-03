from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List
from pathlib import Path
import os

EMBEDDING_NAME = "shibing624/text2vec-base-chinese"
RERANKER_NAME = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
MODEL_DIR = Path("hf_models")

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

class EmbeddingManager:
    """嵌入模型加载"""

    def __init__(self, model_name=EMBEDDING_NAME, model_dir=MODEL_DIR):
        self.model_dir = Path(model_dir)
        self.model_path = self.model_dir / model_name.replace("/", "_")

        # 检测是否存在已下载模型
        if self.model_path.exists():
            self.model = SentenceTransformer(str(self.model_path))
        else:
            self.model_dir.mkdir(parents=True, exist_ok=True)
            self.model = SentenceTransformer(model_name)
            self.model.save(str(self.model_path))

    def encode(self, texts: List[str] | str):
        """生成嵌入向量"""
        return self.model.encode(texts, show_progress_bar=False).tolist()


class RerankerManager:
    """重排序模型加载"""

    def __init__(self, model_name=RERANKER_NAME, model_dir=MODEL_DIR):
        self.model_dir = Path(model_dir)
        self.model_path = self.model_dir / model_name.replace("/", "_")

        # 检测是否存在已下载模型
        if self.model_path.exists():
            self.model = CrossEncoder(str(self.model_path))
        else:
            self.model_dir.mkdir(parents=True, exist_ok=True)
            self.model = CrossEncoder(model_name)
            self.model.save(str(self.model_path))

    def rank(self, query: str, documents: List[str]):
        """对候选文档进行重排序"""
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        ranked_results = sorted(
            [
                {"index": i, "document": {"text": doc}, "relevance_score": score}
                for i, (doc, score) in enumerate(zip(documents, scores))
            ],
            key=lambda x: x["relevance_score"],
            reverse=True,
        )
        return ranked_results


if __name__ == "__main__":
    query = "夏天最好吃的水果是？"
    docs = ["西瓜", "苹果", "香蕉", "橘子", "芒果", "草莓", "葡萄", "菠萝", "荔枝"]
    reranker = RerankerManager()
    results = reranker.rank(query, docs)
    for res in results:
        print(f"文档: {res['document']}, 相关性得分: {res['relevance_score']}")

    embedding = EmbeddingManager()
    texts = [
        "今天天气真好！",
        "我喜欢学习编程。",
    ]
    vectors = embedding.encode(texts)
    for text, vec in zip(texts, vectors):
        print(text, vec[:5], "...", len(vec))
