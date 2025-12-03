from parse_file import parse_file
from pathlib import Path
import re
import json
from openai import OpenAI
import os

client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

PROMPT_TEMPLATE = """你是一名专业的课程助教。

我将提供一段课程讲稿，请你基于内容生成 0~3 个高质量的用于SFT微调的“问题+答案”对。

规则：
1. 每个问题聚焦一个具体知识点；
2. 每个答案必须来自文本内容，不得凭空编造；
3. 问题应覆盖不同角度（定义、原因、过程、应用、区别等）；
4. 输出格式必须严格如下：
问题：<问题1>
答案：<答案1>
问题：<问题2>
答案：<答案2>
...

以下是讲稿内容：
---
{{text_segment}}
"""

def generate_qa(file_path: Path, outdir: Path):
    text = parse_file(file_path, file_path.suffix.lstrip(".").lower())
    segments = split_text(text)
    outpath = outdir / f"{file_path.stem}_qa.jsonl"
    with open(outpath, "w", encoding="utf-8") as fout:
        for seg in segments:
            prompt = PROMPT_TEMPLATE.replace("{{text_segment}}", seg.strip())
            completion = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            text_out = completion.choices[0].message.content
            matches = re.findall(r"问题[:：](.+?)答案[:：](.+?)(?=问题[:：]|$)", text_out, re.S)
            if matches:
                for question, answer in matches:
                    item = {"instruction": question.strip(), "input": "", "output": answer.strip()}
                    fout.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"问答对生成完毕：{outpath}")

def split_text(text, max_len=400):
    """分割文本为多个部分，每部分不超过指定长度。"""
    parts, buf = [], ""
    for s in re.split(r"[。！？\n]", text):
        if not s.strip(): continue
        buf += s + "。"
        if len(buf) > max_len:
            parts.append(buf.strip())
            buf = ""
    if buf:
        parts.append(buf.strip())
    return parts

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="从输入目录生成 QA jsonl 并合并到输出目录")
    parser.add_argument("--raw-dir", "-r", dest="input_dir", default="train_raw", help="原始输入目录（默认: train_raw）")
    parser.add_argument("--out-dir", "-o", dest="output_dir", default="train_data", help="输出目录（默认: train_data）")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_path in input_dir.iterdir():
        generate_qa(file_path, output_dir)
        
    merged = output_dir / "merged.jsonl"
    seen = set()
    with open(merged, "w", encoding="utf-8") as wf:
        for p in sorted(output_dir.iterdir()):
            if not p.is_file() or p.suffix != ".jsonl" or p == merged:
                continue
            with open(p, "r", encoding="utf-8") as rf:
                for line in rf:
                    line = line.strip()
                    if not line or line in seen:
                        continue
                    seen.add(line)
                    wf.write(line + "\n")
    print(f"生成完毕：{merged}")
