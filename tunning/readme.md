# 微调垂直大模型

1. 进入微调文件夹

```bash
cd tunning
```

2. 安装依赖

```bash
pip install -r requirements
```

3. 生成问答对

```bash
cd tunning
python qa.py
    --raw-dir <path_to_raw_data>
    --out-dir <path_to_output_data>
```

4. 微调模型

```bash
python tuning.py
    --base_model Qwen/Qwen3-7B
    --dataset dataset.jsonl
    --output_dir ./ckpts
    --output_log ./logs
    --output_lora ./lora_adapter
    --output_base ./base_model
    --epochs 3
    --batch_size 8
    --accum_steps 2
    --lr 2e-5
    --max_length 512
    --save_base_model

# 启动 TensorBoard 查看日志
tensorboard --logdir logs/
```

5. 部署

```bash
python -m vllm.entrypoints.api_server \
  --model ./base_model \
  --model-name my_model \
  --lora-modules ./lora_adapter \
  --port 8888
```

6. 调用

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model":"my_model",
        "lora":"lora-finetune",
        "messages":[{"role":"user","content":"你好"}]
      }'
```

或

```python
from openai import OpenAI
client = OpenAI(
    api_key="dummy",
    base_url="http://localhost:8000/v1"
)
response = client.chat.completions.create(
    model="my_model,
    messages=[{"role":"user","content":"你好"}],
)
```
