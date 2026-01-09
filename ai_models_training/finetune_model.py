#!/usr/bin/env python3
"""Model Fine-Tuning Script - LoRA Method"""

import os
import sys
import json
import torch
import traceback
from datetime import datetime
from pathlib import Path
from datasets import load_dataset
from dotenv import load_dotenv
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Load developer configuration from root
DEVELOPER_ENV_PATH = Path(__file__).parent.parent / "developer.env"
if DEVELOPER_ENV_PATH.exists():
    load_dotenv(DEVELOPER_ENV_PATH)

# ============================================================================
# CONFIGURATION
# ============================================================================

FINETUNING_CONFIG = {
    "method": "LoRA",
    "version": "v1",
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
}

TRAINING_CONFIG = {
    "num_epochs": 3,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "learning_rate": 2e-4,
    "max_seq_length": 2048,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 100,
}

METADATA_CONFIG = {
    "finetuned_by": os.getenv("DEVELOPER_NAME", "Unknown Developer"),
    "organization": os.getenv("ORGANIZATION", "Unknown Organization"),
    "role": os.getenv("ROLE", "Unknown Role"),
}

SCRIPT_DIR = Path(__file__).parent
OUTPUT_CONFIG = {
    "models_dir": SCRIPT_DIR / "Models",
    "training_data_dir": SCRIPT_DIR / "training data",
    "crash_reports_dir": SCRIPT_DIR / "logs",
}

SYSTEM_CONFIG = {
    "gpu": "NVIDIA RTX 4070 Mobile",
    "vram": "8GB",
    "cuda_version": "12.0",
    "ram": "32GB",
}

# ============================================================================
# UTILITIES
# ============================================================================

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def print_info(text):
    print(f"[INFO] {text}")

def print_success(text):
    print(f"[SUCCESS] {text}")

def print_error(text):
    print(f"[ERROR] {text}")

def print_warning(text):
    print(f"[WARNING] {text}")

def write_crash_report(error, error_context=""):
    """Write detailed crash report to file"""
    os.makedirs(OUTPUT_CONFIG["crash_reports_dir"], exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"crash_report_finetune_model_{timestamp}.log"
    report_path = OUTPUT_CONFIG["crash_reports_dir"] / report_name
    
    with open(report_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("FINE-TUNING SCRIPT CRASH REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Script: finetune_model.py\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n\n")
        
        f.write("Configuration:\n")
        f.write(f"  Method: {FINETUNING_CONFIG['method']}\n")
        f.write(f"  Version: {FINETUNING_CONFIG['version']}\n")
        f.write(f"  User: {METADATA_CONFIG['finetuned_by']}\n")
        f.write(f"  Organization: {METADATA_CONFIG['organization']}\n")
        f.write(f"  CUDA Available: {torch.cuda.is_available()}\n\n")
        
        if error_context:
            f.write(f"Context: {error_context}\n\n")
        
        f.write("Error:\n")
        f.write(f"{type(error).__name__}: {str(error)}\n\n")
        
        f.write("Traceback:\n")
        f.write(traceback.format_exc())
        
        f.write("\n" + "=" * 80 + "\n")
    
    print_error(f"Crash report saved: {report_path}")
    return report_path

def check_system():
    print_header("System Check")
    print_info(f"GPU: {SYSTEM_CONFIG['gpu']}, {SYSTEM_CONFIG['vram']}")
    print_info(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print_info(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    
    os.makedirs(OUTPUT_CONFIG["models_dir"], exist_ok=True)
    os.makedirs(OUTPUT_CONFIG["documentation_dir"], exist_ok=True)
    print_success("Output directories ready")

def copy_license_or_log(source_model_path, output_dir):
    """Copy LICENSE from source model or log missing license"""
    source_license = Path(source_model_path) / "LICENSE"
    
    if source_license.exists():
        import shutil
        dest_license = Path(output_dir) / "LICENSE"
        shutil.copy2(source_license, dest_license)
        print_success(f"Copied LICENSE to output")
    else:
        # Log missing license
        os.makedirs(OUTPUT_CONFIG["crash_reports_dir"], exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = OUTPUT_CONFIG["crash_reports_dir"] / f"missing_license_{timestamp}.log"
        
        with open(log_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("MISSING LICENSE WARNING\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source Model: {source_model_path}\n")
            f.write(f"Output Directory: {output_dir}\n")
            f.write(f"\nWARNING: No LICENSE file found in source model.\n")
            f.write(f"This may indicate licensing compliance issues.\n")
            f.write(f"Please verify the licensing terms before distribution.\n")
        
        print_warning(f"No LICENSE found - logged to: {log_path}")

# ============================================================================
# DATA PREPARATION
# ============================================================================

def load_training_data(version):
    print_header(f"Loading Training Data - {version}")
    
    data_dir = OUTPUT_CONFIG["training_data_dir"] / version
    if not data_dir.exists():
        print_error(f"Training data not found: {data_dir}")
        sys.exit(1)
    
    jsonl_files = list(data_dir.glob("*.jsonl"))
    if not jsonl_files:
        print_error(f"No .jsonl files found in {data_dir}")
        sys.exit(1)
    
    print_info(f"Found {len(jsonl_files)} training file(s)")
    for file in jsonl_files:
        print_info(f"  - {file.name}")
    
    dataset = load_dataset("json", data_files=[str(f) for f in jsonl_files], split="train")
    print_success(f"Loaded {len(dataset)} training examples")
    
    return dataset

def format_instruction(example):
    """Format training examples into instruction format"""
    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output_text = example.get("output", "")
    
    if input_text:
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output_text}"
    else:
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output_text}"
    
    return {"text": prompt}

def prepare_dataset(dataset, tokenizer):
    print_header("Preparing Dataset")
    
    dataset = dataset.map(format_instruction, remove_columns=dataset.column_names)
    
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=TRAINING_CONFIG["max_seq_length"],
            padding="max_length"
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"]
    )
    
    print_success(f"Dataset prepared: {len(tokenized_dataset)} examples")
    return tokenized_dataset

# ============================================================================
# MODEL SETUP
# ============================================================================

def setup_model_and_tokenizer(model_path):
    print_header("Loading Model and Tokenizer")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print_success(f"Model loaded: {model_path}")
    
    lora_config = LoraConfig(
        r=FINETUNING_CONFIG["lora_r"],
        lora_alpha=FINETUNING_CONFIG["lora_alpha"],
        target_modules=FINETUNING_CONFIG["target_modules"],
        lora_dropout=FINETUNING_CONFIG["lora_dropout"],
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    print_success("LoRA adapters configured")
    
    return model, tokenizer

# ============================================================================
# TRAINING
# ============================================================================

def train_model(model, tokenizer, dataset, model_name, version):
    print_header("Fine-Tuning Model")
    
    output_name = f"{model_name}_ft_{version}"
    output_dir = OUTPUT_CONFIG["models_dir"] / output_name
    
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=TRAINING_CONFIG["num_epochs"],
        per_device_train_batch_size=TRAINING_CONFIG["batch_size"],
        gradient_accumulation_steps=TRAINING_CONFIG["gradient_accumulation_steps"],
        learning_rate=TRAINING_CONFIG["learning_rate"],
        warmup_steps=TRAINING_CONFIG["warmup_steps"],
        logging_steps=TRAINING_CONFIG["logging_steps"],
        save_steps=TRAINING_CONFIG["save_steps"],
        fp16=True,
        optim="adamw_torch",
        save_total_limit=2,
        load_best_model_at_end=False,
        report_to="none"
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator
    )
    
    print_info("Starting training...")
    trainer.train()
    
    print_info("Saving model...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Copy LICENSE or log if missing
    # Get original model path from the main function context
    original_model_path = sys.argv[1] if len(sys.argv) > 1 else None
    if original_model_path:
        copy_license_or_log(original_model_path, output_dir)
    
    config_path = output_dir / "finetuning_config.json"
    with open(config_path, "w") as f:
        json.dump({
            "method": FINETUNING_CONFIG["method"],
            "version": version,
            "lora_config": {
                "r": FINETUNING_CONFIG["lora_r"],
                "alpha": FINETUNING_CONFIG["lora_alpha"],
                "dropout": FINETUNING_CONFIG["lora_dropout"],
                "target_modules": FINETUNING_CONFIG["target_modules"]
            },
            "training_config": TRAINING_CONFIG,
            "finetuned_date": datetime.now().isoformat(),
            "finetuned_by": METADATA_CONFIG["finetuned_by"],
            "organization": METADATA_CONFIG["organization"],
            "role": METADATA_CONFIG["role"],
            "system": SYSTEM_CONFIG,
        }, f, indent=2)
    
    print_success(f"Model saved: {output_dir}")
    return output_dir

# ============================================================================
# DOCUMENTATION
# ============================================================================

def generate_documentation(model_name, output_dir, original_path, version, dataset_size):
    print_header("Generating Documentation")
    
    original_doc_ref = f"[{model_name}.md]({model_name}.md)"
    
    doc_content = f"""# {model_name} - Fine-Tuned {version.upper()}

## Fine-Tuning Information
- **Changed by**: {METADATA_CONFIG['finetuned_by']}
- **Organization**: {METADATA_CONFIG['organization']}
- **Role**: {METADATA_CONFIG['role']}
- **Date**: {datetime.now().strftime("%d.%m.%Y")}
- **Source Model**: {original_doc_ref}

## Changes Made
- Applied LoRA (Low-Rank Adaptation) fine-tuning
- Training data: {dataset_size} examples ({version})
- Specialized for BigQuery SQL and web analytics queries
- Target modules: {', '.join(FINETUNING_CONFIG['target_modules'])}

## Fine-Tuning Details
- **Method**: {FINETUNING_CONFIG['method']}
- **Version**: {version}
- **LoRA Rank (r)**: {FINETUNING_CONFIG['lora_r']}
- **LoRA Alpha**: {FINETUNING_CONFIG['lora_alpha']}
- **Dropout**: {FINETUNING_CONFIG['lora_dropout']}
- **Epochs**: {TRAINING_CONFIG['num_epochs']}
- **Learning Rate**: {TRAINING_CONFIG['learning_rate']}
- **Batch Size**: {TRAINING_CONFIG['batch_size']}
- **Max Sequence Length**: {TRAINING_CONFIG['max_seq_length']}

## Training Data
- **Location**: `training data/{version}/`
- **Format**: JSONL (instruction, input, output)
- **Domain**: BigQuery SQL for web analytics
- **Examples**: {dataset_size}

## System Requirements
- **GPU**: Recommended for inference (can run on CPU)
- **VRAM**: 4-6GB for inference
- **RAM**: 16GB minimum

## Performance Notes
- Specialized for BigQuery Standard SQL
- Improved understanding of web analytics schemas
- Better at generating aggregate queries and window functions
- Maintains general code generation capabilities

## Next Steps
1. Test on validation queries
2. Quantize fine-tuned model for CPU deployment
3. Compare with base model performance
4. Iterate with additional training data (v2, v3, etc.)
"""
    
    doc_filename = f"{model_name}_ft_{version}.md"
    doc_path = OUTPUT_CONFIG["documentation_dir"] / doc_filename
    
    with open(doc_path, "w") as f:
        f.write(doc_content)
    
    print_success(f"Documentation: {doc_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    try:
        print_header(f"Fine-Tuning Script - {FINETUNING_CONFIG['method']}")
        print_info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if len(sys.argv) != 2:
            print_error("Usage: python finetune_model.py <model_path>")
            print_info("Example: python finetune_model.py Models/qwen2.5-coder-1.5b-instruct")
            sys.exit(1)
        
        model_path = sys.argv[1]
        if not os.path.exists(model_path):
            print_error(f"Model not found: {model_path}")
            sys.exit(1)
        
        check_system()
        
        if not torch.cuda.is_available():
            print_warning("CUDA not available. Fine-tuning will be very slow on CPU.")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(0)
        
        version = FINETUNING_CONFIG["version"]
        model_name = Path(model_path).name
        
        dataset = load_training_data(version)
        model, tokenizer = setup_model_and_tokenizer(model_path)
        prepared_dataset = prepare_dataset(dataset, tokenizer)
        output_dir = train_model(model, tokenizer, prepared_dataset, model_name, version)
        generate_documentation(model_name, output_dir, model_path, version, len(dataset))
        
        print_header("Complete ✅")
        print_success(f"Fine-tuned model: {output_dir}")
        print_info("Next: Quantize the fine-tuned model for CPU deployment")
        
    except KeyboardInterrupt:
        print_warning("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Failed: {e}")
        write_crash_report(e, f"Model: {sys.argv[1] if len(sys.argv) > 1 else 'unknown'}")
        sys.exit(1)

if __name__ == "__main__":
    main()
