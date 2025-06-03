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
    - Device used for testing: Ryzen 9 6900HX 8C16T, 32GB, RTX 3060 12GB PCIe x4 4.0 (Oculink)

**How this works?**


## Instruction

**Step 1: Run Ollama as a service**
- `ollama serve` this will run Ollama on `localhost:11434`, allowing API access.
- `python src/modules/ollama_commenter/ollama_commenter.py /path/to/code [--model model_name] [--ext .vue --ext .dart]`