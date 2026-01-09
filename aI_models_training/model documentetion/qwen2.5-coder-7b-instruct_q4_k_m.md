# qwen2.5-coder-7b-instruct - GGUF Q4_K_M

## Quantization Information
- **Changed by**: Per Erik Grønvik
- **Organization**: OsloMet
- **Role**: Student
- **Date**: 09.01.2026
- **Source Model**: [qwen2.5-coder-7b-instruct.md](qwen2.5-coder-7b-instruct.md)

## Changes Made
- Converted from HuggingFace format to GGUF format
- Quantized from FP16 to Q4_K_M (4-bit, medium quality)
- Optimized for CPU-only deployment

## CPU-Only Deployment

## Quantization Details
- **Method**: GGUF Q4_K_M
- **Description**: 4-bit, medium quality
- **Quality**: Excellent
- **Speed**: Fast

## Model Sizes
- **Original**: 14.20 GB
- **Quantized**: 4.36 GB
- **Reduction**: 69.3%
- **RAM Required**: ~6-8GB

## System Requirements
- **Target**: CPU-only (no GPU)
- **RAM**: 16GB minimum for Q4_K_M
- **CPU**: 8+ CPU threads

## Files
- `qwen2.5-coder-7b-instruct-Q4_K_M.gguf` - Quantized model
- `qwen2.5-coder-7b-instruct-f16.gguf` - FP16 version
- `quantization_config.json` - Configuration

## Status
✅ Success
