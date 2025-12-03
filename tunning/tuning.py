from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    TrainerCallback,
)
from peft import LoraConfig, get_peft_model
import torch
import os
import argparse

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


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


def prepare_data(tokenizer, dataset, max_length=512):
    """数据预处理函数"""

    def preprocess_function(examples):
        texts = []
        for instr, inp, out in zip(
            examples["instruction"], examples["input"], examples["output"]
        ):
            if inp:
                text = f"用户：{instr}\n上下文：{inp}\n助教：{out}"
            else:
                text = f"用户：{instr}\n助教：{out}"
            texts.append(text)

        tokenized = tokenizer(
            texts, truncation=True, max_length=max_length, padding="max_length"
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        for i, mask in enumerate(tokenized["attention_mask"]):
            tokenized["labels"][i] = [
                lid if m == 1 else -100 for lid, m in zip(tokenized["labels"][i], mask)
            ]
        return tokenized

    return dataset.map(preprocess_function, batched=True)


def main(args):
    # --------------------
    # 加载基础模型与 tokenizer
    # --------------------
    print(f"正在加载基础模型：{args.base_model}")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(args.base_model, device_map="auto")
    if args.save_base:
        print(f"保存基础模型到：{args.output_base}")
        model.save_pretrained(args.output_base)
        tokenizer.save_pretrained(args.output_base)

    # --------------------
    # 应用 LoRA
    # --------------------
    print("正在应用 LoRA...")
    lora_cfg = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=args.target_modules.split(","),
        lora_dropout=args.lora_dropout,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    # --------------------
    # 加载数据集
    # --------------------
    print(f"正在加载数据集：{args.dataset}")
    dataset = load_dataset(args.dataset, split="train")
    tokenized = prepare_data(tokenizer, dataset, max_length=args.max_length)

    # --------------------
    # 训练
    # --------------------
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.accum_steps,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        logging_steps=10,
        logging_dir=args.output_log,
        fp16=True,
        save_strategy="epoch",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
    )

    trainer.train()

    # --------------------
    # 保存 LoRA 适配器
    # --------------------
    print(f"保存 LoRA 适配器到：{args.output_lora}")
    model.save_pretrained(args.output_lora)
    tokenizer.save_pretrained(args.output_lora)

    # --------------------
    # 可选：将 LoRA 合并到基础模型
    # --------------------
    if args.merge:
        print("正在将 LoRA 合并到基础模型...")
        merged_model = model.merge_and_unload()
        merged_model.save_pretrained(args.output_merged)
        tokenizer.save_pretrained(args.output_merged)
        print(f"合并后的模型已保存到：{args.output_merged}")

    print("完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # 基础模型
    parser.add_argument("--base_model", type=str, required=True)

    # 数据集
    parser.add_argument("--dataset", type=str, required=True)

    # 训练参数
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--accum_steps", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max_length", type=int, default=512)

    # LoRA 参数
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--lora_dropout", type=float, default=0.05)
    parser.add_argument("--target_modules", type=str, default="q_proj,v_proj")

    # 输出路径
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
    parser.add_argument("--output_log", type=str, default="./logs")
    parser.add_argument("--output_lora", type=str, default="./lora_adapter")
    parser.add_argument("--output_base", type=str, default="./base_model")
    parser.add_argument("--output_merged", type=str, default="./merged_model")

    # 选项
    parser.add_argument("--merge", action="store_true", help="Merge model")
    parser.add_argument("--save_base", action="store_true", help="Save base model")

    args = parser.parse_args()
    main(args)
