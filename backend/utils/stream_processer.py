import json
import os
from typing import List
from sqlalchemy.orm import Session
from .ai_client import client, chat_once, get_rerank
import models_.ai_assistant as models
from .chroma_manager import VectorStore


def get_docs(query: str, top_K1=10, top_K2=3) -> List[str]:
    """从向量数据库获取相关文本块"""
    vs = VectorStore()
    results = vs.query(query, top_k=top_K1)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    ids = results["ids"][0]

    _results = get_rerank(query, docs)[:top_K2]
    results = []
    for result in _results:
        if result["relevance_score"] > 0:
            results.append(
                {
                    "doc": docs[result["index"]],
                    "filename": metas[result["index"]].get("filename", ""),
                    "filepath": metas[result["index"]].get("filepath", ""),
                    "fileid": metas[result["index"]].get("fileid", ""),
                    "doc_id": ids[result["index"]],
                    "score": result["relevance_score"],
                }
            )

    return results


class StreamProcessor:
    def __init__(self, db: Session, conv_id: str, user_input: str):
        self.stream = []
        self.db = db
        self.conv_id = conv_id
        self._save_query_message(user_input)

        docs = get_docs(user_input)
        seen = set()
        self.doc_info = []
        for d in docs:
            key = d.get("fileid") or (d.get("filename"), d.get("filepath"))
            if key in seen:
                continue
            seen.add(key)
            self.doc_info.append(
                {
                    "filename": d.get("filename"),
                    "filepath": d.get("filepath"),
                    "fileid": d.get("fileid"),
                }
            )
        # 从数据库中获取最近10条消息作为上下文
        db_messages = (
            db.query(models.Message)
            .filter(models.Message.conversation_id == conv_id)
            .order_by(models.Message.created_at.desc())
            .limit(10)
            .all()
        )
        self.messages_payload = [
            {"role": m.role, "content": m.content} for m in db_messages[::-1]
        ]
        self.messages_payload[-1]["content"] = (
            f"根据以下相关片段，简要回答用户的问题。"
            + f"相关片段：{chr(10).join([d.get('doc') for d in docs])}"
            + f"用户问题：{user_input}"
        )
        with open("debug_messages.json", "w", encoding="utf-8") as f:
            json.dump(self.messages_payload, f, ensure_ascii=False, indent=2)

    def generate_stream(self):
        yield f"data: {json.dumps({'begin': True, 'conv_id': self.conv_id})}\n\n"
        try:
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=self.messages_payload,
                stream=True,
            )
            for chunk in response:
                if not chunk.choices or len(chunk.choices) == 0:
                    continue
                delta = getattr(chunk.choices[0], "delta", None)
                content = getattr(delta, "content", None)
                if content:
                    self.stream.append(content)
                    yield f"data: {json.dumps({'content': content})}\n\n"
            self._save_reply_message()
            yield f"data: {json.dumps({'done': True, 'rag_docs': self.doc_info})}\n\n"
        except Exception as e:
            print(f"Error during streaming: {e}")
            yield f"data: [Error occurred: {e}]\n\n"

    def _save_query_message(self, user_input: str):
        msg = models.Message(
            conversation_id=self.conv_id,
            role="user",
            content=user_input,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def _save_reply_message(self):
        answer = "".join(self.stream)
        msg = models.Message(
            conversation_id=self.conv_id,
            role="assistant",
            content=answer,
            rag_docs=self.doc_info,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg


if __name__ == "__main__":
    question = "大数据的多样性指什么？"
    results = get_docs(question)
    docs = [r["doc"] for r in results]
    answer = chat_once(
        "根据以下相关片段，简要回答用户的问题。\n\n" + 
        f"相关片段：\n{chr(10).join(docs)}\n\n" + 
        f"用户问题：{question}\n\n" + 
        "请给出回答。"
    )
    print("问题：", question)
    print("相关文档：")
    for r in results:
        print(f"\t文档ID: {r['doc_id']}\t分数: {r['score']}\t元数据: {r['filename']}, {r['filepath']}")
        print(f"\t内容: {r['doc'][:10].replace(chr(10), '')}...")
    print("回答：", answer)
