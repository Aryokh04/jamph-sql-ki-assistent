# Quantization Details

## Process Information
- **Date**: 2026-01-09 20:19:11
- **Method**: GGUF Q4_K_M
- **Quantized by**: Per Erik Grønvik
- **Organization**: OsloMet
- **Role**: Student

## Source Model
- **Path**: `ai_models_training/model training/Models/qwen2.5-coder-1.5b-instruct`
- **Type**: Original model

## Quantization Method: Q4_K_M
- **Description**: 4-bit, medium quality
- **Size Reduction**: ~75%
- **Quality**: Excellent
- **Speed**: Fast
- **RAM Required**: ~6-8GB

## Results
- **Original Size**: 2.89 GB
- **Quantized Size**: 0.92 GB
- **Actual Reduction**: 68.2%

## System Configuration

### Source System
- **GPU**: NVIDIA RTX 4070 Mobile
- **VRAM**: 8GB
- **RAM**: 32GB
- **CUDA**: 12.0

### Target System (Deployment)
- **Device**: CPU Only
- **RAM**: 16GB minimum for Q4_K_M
- **CPU**: 8+ CPU threads

## Conversion Steps
1. Converted HuggingFace model to GGUF FP16
2. Quantized FP16 to Q4_K_M
3. Removed intermediate FP16 file
4. Generated Ollama Modelfile

## Status
✅ Quantization completed successfully
