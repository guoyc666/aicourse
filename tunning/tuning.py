from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, TrainerCallback
from peft import LoraConfig, get_peft_model
import torch

class LoggingCallback(TrainerCallback):
    """在 Trainer logging 时打印关键信息到控制台"""
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is None:
            return
        step = logs.get("step", state.global_step)
        loss = logs.get("loss")
        lr = logs.get("learning_rate") or logs.get("lr")
        if loss is not None:
            print(f"[step {step}] loss={loss:.6f}" + (f" lr={lr:.3e}" if lr else ""))
        else:
            print(f"[step {step}] logs={logs}")

    def on_epoch_end(self, args, state, control, **kwargs):
        epoch = int(state.epoch) if state.epoch is not None else "?"
        print(f"=== epoch {epoch} finished. global_step={state.global_step} ===")

# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
MODEL_NAME = "Qwen/Qwen2.5-7B"        # 模型名称
DATA_PATH = "merged.jsonl"     # 训练数据路径
OUTPUT_DIR = "models/ft_Qwen_Qwen2.5-7B"         # 输出模型目录
LOCAL_BASE_DIR = "models/Qwen2.5-7B"

# 加载数据
dataset = load_dataset("json", data_files=DATA_PATH, split="train")

tokenizer = AutoTokenizer.from_pretrained(LOCAL_BASE_DIR)
model = AutoModelForCausalLM.from_pretrained(
        LOCAL_BASE_DIR,
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )

# 数据预处理
def preprocess_function(examples):
    """批量处理多个样本"""
    texts = []
    for instr, inp, out in zip(examples["instruction"], examples["input"], examples["output"]):
        if inp:
            text = f"用户：{instr}\n上下文：{inp}\n助教：{out}"
        else:
            text = f"用户：{instr}\n助教：{out}"
        texts.append(text)

    tokenized = tokenizer(
        texts,
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    for i, mask in enumerate(tokenized["attention_mask"]):
        tokenized["labels"][i] = [lid if m==1 else -100 for lid, m in zip(tokenized["labels"][i], mask)]
    return tokenized

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# 配置LoRA微调
lora_config = LoraConfig(
    r=32,                    # 低秩矩阵维度（控制可训练参数量）
    lora_alpha=32,          # 缩放因子（控制LoRA更新强度）
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # 覆盖注意力投影层
    lora_dropout=0.05,      # 防止过拟合
    bias="none",            # 不使用额外偏置
    task_type="CAUSAL_LM"   # 因果语言建模任务
)

model = get_peft_model(model, lora_config)

# 训练配置
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=5,
    warmup_ratio=0.05,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to=["tensorboard"],
    logging_dir="logs"
)

# 训练器
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    callbacks=[LoggingCallback()] 
)

# 启动训练
trainer.train()

# 保存模型
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("微调完成，模型保存在:", OUTPUT_DIR)