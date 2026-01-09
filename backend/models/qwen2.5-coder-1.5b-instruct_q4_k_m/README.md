# qwen2.5-coder-1.5b-instruct_q4_k_m - Docker Deployment

## Overview
This directory contains the Docker deployment artifacts for the qwen2.5-coder-1.5b-instruct_q4_k_m model.

**Original Model:** Unknown  
**Quantization:** Unknown  
**Dockerized by:** Per Erik Grønvik  
**Organization:** OsloMet  
**Date:** 2026-01-09

## Quick Start

### Build and Run
```bash
# From project root
docker-compose up -d qwen2.5-coder-1.5b-instruct_q4_k_m
```

### Test the Model
```bash
# Check if container is running
docker ps | grep qwen2.5-coder-1.5b-instruct_q4_k_m

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder-1.5b-instruct_q4_k_m",
  "prompt": "Write a SQL query to select all users:",
  "stream": false
}'
```

### Stop the Container
```bash
docker-compose down qwen2.5-coder-1.5b-instruct_q4_k_m
```

## Files
- `Dockerfile` - Container definition
- `qwen2.5-coder-1.5b-instruct_q4_k_m.gguf` - Quantized model (GGUF format)
- `Modelfile` - Ollama model configuration
- `LICENSE` - Model license
- `README.md` - This file

## API Usage

### Generate Text
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder-1.5b-instruct_q4_k_m",
  "prompt": "Your prompt here",
  "stream": false
}'
```

### Chat Completion
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5-coder-1.5b-instruct_q4_k_m",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}'
```

## Configuration

### Environment Variables
- `OLLAMA_HOST`: Server address (default: 0.0.0.0:11434)
- `OLLAMA_MODELS`: Model storage path (default: /root/.ollama)
- `OLLAMA_NUM_PARALLEL`: Parallel requests (default: 1)

### Resource Requirements
- **RAM:** 8GB minimum
- **CPU:** 8+ threads recommended
- **Storage:** Unknown

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs qwen2.5-coder-1.5b-instruct_q4_k_m

# Verify model creation
docker exec qwen2.5-coder-1.5b-instruct_q4_k_m ollama list
```

### Port already in use
Edit `docker-compose.yml` to use different port:
```yaml
ports:
  - "11435:11434"  # Changed from 11434
```

## Development

### Rebuild Container
```bash
docker-compose build qwen2.5-coder-1.5b-instruct_q4_k_m
docker-compose up -d qwen2.5-coder-1.5b-instruct_q4_k_m
```

### Access Container Shell
```bash
docker exec -it qwen2.5-coder-1.5b-instruct_q4_k_m /bin/bash
```

## Related Files
- Source quantization: `ai_models_training/Models/qwen2.5-coder-1.5b-instruct_q4_k_m/`
- Model documentation: See source directory for QUANTIZATION.md
