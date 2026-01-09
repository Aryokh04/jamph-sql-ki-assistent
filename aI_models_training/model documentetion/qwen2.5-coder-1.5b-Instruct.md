# Qwen2.5-Coder 1.5B Instruct

## Model Information

- **Developer**: Alibaba Cloud / Qwen Team
- **Model ID**: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- **Release Date**: September 2024
- **Model Size**: 1.5 billion parameters (~3GB)
- **License**: Apache 2.0
- **Context Length**: 128k tokens
- **Specialization**: Code generation and programming tasks
- **Downloaded**: 09.01.2026
- **Downloaded by**: Per Erik Grønvik
- **Organization**: OsloMet
- **Role**: Student

## Overview

Qwen2.5-Coder is a specialized coding model from the Qwen2.5 series, specifically optimized for programming tasks including SQL, BigQuery, Python, and other programming languages. It is fine-tuned for instruction following in coding contexts.

## Key Features

- **Code-Specialized Training**: Trained on 5.5 trillion tokens of code-related data
- **SQL Excellence**: Strong performance on SQL query generation, debugging, and optimization
- **BigQuery Support**: Understanding of BigQuery Standard SQL, functions, and best practices
- **Multi-Language Support**: Python, JavaScript, Java, SQL, and 80+ programming languages
- **Extended Context**: 128k token context window for large codebases
- **Instruction Following**: Fine-tuned for following coding instructions accurately

## Model Files

- `model.safetensors` - Model weights in SafeTensors format (split files)
- `config.json` - Model configuration
- `tokenizer.json` - Tokenizer configuration
- `generation_config.json` - Generation parameters

## Recommended Settings for SQL Generation

## Resources

- **Official Documentation**: https://github.com/QwenLM/Qwen2.5
- **Hugging Face Hub**: https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct
- **Model Card**: Available on Hugging Face
- **Blog Post**: https://qwenlm.github.io/blog/qwen2.5-coder/

## Training Data

### Data Scale and Composition

- **Code-Specific Training**: 5.5 trillion tokens of code-related data
- **Programming Languages**: 80+ languages including SQL, Python, JavaScript, Java, C++, etc.
- **Code Sources**: "Publicly available code repositories and datasets"
- **Context**: Large context windows from real-world codebases
- **SQL Coverage**: Includes SQL queries, database schemas, and data transformation code
- **Knowledge Cutoff**: Training data up to mid-2024

### Legal and Copyright Considerations

**License**: Apache 2.0 (fully open for commercial use)

**Training Data Copyright Status in the EU**:
- Described as "publicly available code repositories and online data"
- **No specific disclosure** of which repositories, datasets, or codebases were used
- **No explicit statement** about GitHub public repositories, Stack Overflow, or other sources
- **No compensation agreements disclosed** with original code authors

**Important Legal Notes**:
1. **Code Training Data**: Likely includes code from public repositories (GitHub, GitLab, etc.)
2. **License Diversity**: Public code repositories contain various licenses (MIT, Apache, GPL, proprietary)
3. **Attribution**: Training on open-source code doesn't automatically comply with license attribution requirements

## Best Practices for SQL/BigQuery Use

1. **Provide Schema**: Always include table schemas in your prompt
2. **Specify Dialect**: Mention "BigQuery SQL" explicitly for BigQuery-specific features
3. **Be Specific**: Clear requirements lead to better queries
4. **Review Output**: Always validate generated SQL before execution
5. **Iterative Refinement**: Ask for modifications if needed
6. **Performance Context**: Mention performance requirements (e.g., "optimize for large datasets")
7. **Test Queries**: Use LIMIT clauses when testing with production data
