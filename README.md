# Document Generator with Local LLM

## Project Overview

As a software developer, are you tired of writing documents? Who else would need to read this but me? 😒

As a software developer 1 month from now, are you frustrated that you can't understand what you wrote? 🥲

As QA and tester, are you tired of undocumented code? 🤬

But you can't legally share your proprietary code base to LLM like DeepSeek or ChatGPT to document?

Then this is the tool for you. 

👉 Automatically generate documentation (README and code comments) for source code using a local LLM (Deepseek, Qwen, Devstral). 


**Key Features**

- Download and run local LLMs like Qwen, DeepSeep, Devstral or Gemma via Ollama.
- Process source code files recursively from a directory.
- Add comments to clarify code.
- Generate a project README based on the code.
- Document commit/changes for self-documenting Pull Requests.

**Requirements**

1. Ollama installed
    - Download from the official Ollama site: https://ollama.com/download
    - Python library: `pip install ollama`
2. PC requirement
    - The specific PC requirements will depends on the model of your choice. Please refer to specific Ollama models for their requirements: https://ollama.com/search

**How this works?**


## Instruction

**Step 1: Run Ollama as a service**
- `ollama serve` this will run Ollama on `localhost:11434`, allowing API access.

**Step 2:**
- `python ollama_commenter.py /path/to/code --model model_name`
- `python source_code_handler.py /path/to/project`

## Perfomance comparison

Below are some models that was tested and evaluated.

**Note:**
- Some comparison criteria are subjective, one developer might consider a comment too detailed, while another developer might consider that same comment too oversimplified. 
- Larger models will yield higher perfomance, but will requires more computation resources. Some models will requires at least 120+ GB of RAM or they outright refuses to start.

### Comparison 

Each models were tested with 10 programs. Code Understanding and Comment Quality is **my subjective evaluation**

| Model                     | Code Understanding | Comment Quality | Throughput | VRAM Uasge | Limits                                   |
|---------------------------|--------------------|-----------------|------------|------------|------------------------------------------|
| Deepseek-R1:70b           |                    |                 |            |            |                                          |
| Deepseek-R1:8b            |                    |                 |            |            |                                          |
| Devstral:24b              |                    |                 |            |            |                                          |
| Qwen2.5-coder:32b         |                    |                 |            |            |                                          |
| Codellama:70b             |                    |                 |            |            |                                          |
| Deepseek-coder-v2:16b     | 4/5                | 4/5             |            | 2.6 GB     | Struggles with files over ~120 lines     |
| Web-based Deekseek        |                    |                 | NA         | NA         |                                          |
| Web-based ChatGPT         |                    |                 | NA         | NA         |                                          |
| Web-based Grok            |                    |                 | NA         | NA         |                                          |



Also compare the performance against 3 popular web-based LLM: Deepseek, ChatGPT and Grok.

### Criteria explanation

**1. Code Understanding**
- Correctness: Does the comment accurately explain the code's functionality?
- Depth: Does it capture subtle logic, edge cases, and algorithmic complexity?
- Context Awareness: Does it understand project-specific patterns or idioms?

**2. Comment Quality**
- Clarity: Are explanations easy to understand?
- Conciseness: Avoids verbosity while being informative (measure comment-to-code ratio)
- Relevance: Focuses on non-obvious aspects (e.g., explains why more than what)
- Formatting: Proper syntax, placement, and structure for the language

**3. Latency**
- Time from request to completed output, lower is better


