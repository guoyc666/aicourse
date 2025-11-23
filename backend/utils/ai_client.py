import base64
import mimetypes
import httpx
from openai import OpenAI
from openai.types.embedding import Embedding
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_BASE_URL")
)


def chat_stream(messages: list[dict]):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages,
        stream=True,
    )
    for chunk in response:
        # 先判断 choices 是否非空
        if not chunk.choices or len(chunk.choices) == 0:
            continue
        delta = getattr(chunk.choices[0], "delta", None)
        content = getattr(delta, "content", None)
        if content:
            # 使用 SSE 格式发送数据
            yield f"data: {content}\n\n"


def chat_completion(messages: list[dict]):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages,
    )
    return response.choices[0].message.content


def chat_once(message: str):
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[{"role": "user", "content": message}],
        temperature=0.7,
    )
    return resp.choices[0].message.content


xf_client = OpenAI(api_key=os.getenv("XF_API_KEY"), base_url=os.getenv("XF_BASE_URL"))


def get_embedding(
    text: str | list[str], model=os.getenv("EMBEDDING_ID")
) -> list[Embedding]:
    """
    调用 Embedding API。
    :param text: 需要进行向量化的一段或多段文本。
    :param model: 使用的 embedding 模型 ID。
    :return: List[Embedding(embedding: List[float], index: int, object: "embedding")]
    """
    try:
        response = xf_client.embeddings.create(
            model=model,
            input=text,
            # dimensions=768,
        )
        return response.data
    except Exception as e:
        print(f"Embedding 请求出错: {e}")
        return None


def get_rerank(query, documents, model=os.getenv("RERANKER_ID")) -> dict:
    """
    调用 Rerank API。
    :param query: 查询语句。
    :param documents: 需要重排序的文档列表。
    :param model: 使用的 rerank 模型 ID。
    :return: [{'index': int, 'document': {'text': str}, 'relevance_score': float}, ...]
    """
    try:
        # 注意：OpenAI SDK 没有原生的 rerank 方法，需要通过 client.post 发起原始请求
        response = xf_client.post(
            "/rerank",
            body={
                "model": model,
                "query": query,
                "documents": documents,
            },
            cast_to=httpx.Response,
        )
        results = response.json().get("results", [])
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results
    except Exception as e:
        print(f"Rerank 请求出错: {e}")
        return None


def get_image_ocr(image_path: str, model=os.getenv("OCR_ID")) -> str:
    """
    调用 OCR API 进行图片文字识别。
    :param image_path: 图片文件路径。
    :param model: 使用的 OCR 模型 ID。
    :return: 识别出的文本内容。
    """
    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/png"

        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        data_url = f"data:{mime_type};base64,{image_base64}"
        response = xf_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "提取图片内容"},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            temperature=0.7,
            max_tokens=8192,
        )
        result = response.json()
        return result.get("text", "")
    except Exception as e:
        print(f"OCR 请求出错: {e}")
        return ""


if __name__ == "__main__":
    ...
