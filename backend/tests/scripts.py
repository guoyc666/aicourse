from docx import Document
import re
import os

def docx_to_sentences_by_chunk(docx_path, chunk_size=100):
    doc = Document(docx_path)
    text = "".join([para.text for para in doc.paragraphs])
    sentences = []
    idx = 0
    while idx < len(text):
        chunk = text[idx:idx+chunk_size]
        match = list(re.finditer(r'。', chunk))  # 只用中文句号
        if match:
            last_dot = match[-1].end()
            sentence = text[idx:idx+last_dot].strip()
            sentences.append(sentence)
            idx += last_dot
        else:
            next_dot = re.search(r'。', text[idx+chunk_size:])
            if next_dot:
                end_pos = idx + chunk_size + next_dot.end()
                sentence = text[idx:end_pos].strip()
                sentences.append(sentence)
                idx = end_pos
            else:
                sentence = text[idx:].strip()
                if sentence:
                    sentences.append(sentence)
                break
    return sentences

input_dir = "F:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\DOCX讲稿"
output_dir = "F:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\output"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".docx"):
        docx_path = os.path.join(input_dir, filename)
        sentences = docx_to_sentences_by_chunk(docx_path, chunk_size=100)
        output_path = os.path.join(output_dir, filename.replace(".docx", "_sentences.txt"))
        with open(output_path, "w", encoding="utf-8") as f:
            for s in sentences:
                f.write(s + "\n")