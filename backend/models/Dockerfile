# Multi-Model Ollama Dockerfile
# Serves multiple GGUF models from a single container
# Models are loaded on-demand based on API requests

FROM ollama/ollama:latest

# Set working directory
WORKDIR /models

# Copy model files (GGUF + Modelfile)
COPY qwen2.5-coder-1.5b-instruct_q4_k_m/*.gguf ./qwen2.5-coder-1.5b-instruct_q4_k_m/
COPY qwen2.5-coder-1.5b-instruct_q4_k_m/Modelfile ./qwen2.5-coder-1.5b-instruct_q4_k_m/

# Create models in Ollama
# Models will be available via API: {"model": "qwen2.5-coder-1.5b", ...}
RUN ollama serve & \
    sleep 5 && \
    ollama create qwen2.5-coder-1.5b -f /models/qwen2.5-coder-1.5b-instruct_q4_k_m/Modelfile && \
    pkill ollama

# Expose Ollama API port
EXPOSE 11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Start Ollama server
# Note: Use "serve" not "ollama serve" since /bin/ollama is the entrypoint
CMD ["serve"]
