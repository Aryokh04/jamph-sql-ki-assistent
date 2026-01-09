# Ollama Model Server

Single Ollama container serving multiple quantized models on-demand.

## Architecture

- Models load into RAM on first request
- Automatic queuing when concurrent limit reached
- Memory management via environment variables in `docker-compose.yml`

## Deployment

```bash
# From project root
docker-compose up -d ollama

# Check status
docker logs ollama-models

# List available models
curl http://localhost:11434/api/tags
```

## API Usage

```bash
# Generate text
curl http://localhost:11434/api/generate -d '{
  "model": "<model-name>",
  "prompt": "Your prompt",
  "stream": false
}'

# List models
curl http://localhost:11434/api/tags
```

## Configuration

Adjust concurrency and memory in `docker-compose.yml`:
```yaml
environment:
  - OLLAMA_NUM_PARALLEL=1        # Concurrent requests
  - OLLAMA_MAX_LOADED_MODELS=1   # Models kept in RAM
```
