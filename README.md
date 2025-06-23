# Private LLM Code Commenter

An Automated Document Generator using Private and Secured Local LLM

## Project Overview

As a software developer, are you tired of writing documents? Who else would need to read this but me? 😒

As a software developer 1 month from now, are you frustrated that you can't understand what you wrote? 🥲

As QA and tester, are you tired of undocumented code? 🤬

But you can't legally share your proprietary code base to LLM such as DeepSeek or ChatGPT to document? 🔒

Then this is the tool for you. 🙌

Private LLM Code Commenter solves critical documentation challenges for software teams by enabling **secure, privacy-preserving documentation generation** directly within your development environment. This tool empowers developers to:
- Automatically generate comprehensive README files and inline code comments  
- Maintain documentation parity with rapidly evolving codebases  
- Ensure compliance by processing proprietary code locally  
- Streamline onboarding and knowledge transfer  

👉 By leveraging local LLMs (DeepSeek, Qwen, Devstral, etc.) via Ollama, Private LLM Code Commenter keeps sensitive intellectual property secure while delivering enterprise-grade documentation capabilities.

<img src="doc/file_commenter_illustration.png" alt="Alt Text" width="100%"/>

**Key Features**

- **Local Processing**: Runs entirely on your infrastructure - **can run 100% air-gapped, no code leaves your environment**  
- **Multi-Format Support**: Generates READMEs, inline comments, and commit documentation  
- **Model Flexibility**: Compatible with leading LLMs (DeepSeek, Qwen, Gemma, Codellama)  
- **Batch Processing**: Recursive directory handling for entire codebases  

**Requirements**

1. Ollama installed
    - Download from the official Ollama site: https://ollama.com/download
    - Python library: `pip install ollama` `pip install requests`

2. Hardware requirements:
    - The specific PC requirements will depends on the model of your choice: https://ollama.com/search
    - Typical configurations range from 8GB VRAM (7B models) to 120GB+ RAM (70B models)

## Instruction

**Step 1: Launch Ollama service**
- `ollama serve` this will run Ollama on `localhost:11434`, allowing API access.

**Step 2:**

**For single file comment generation**
- `.\file_commenter.bat /path/to/file -m model_name`

**For directory comment generation**
- `.\path_commenter.bat /path/to/code -m model_name`

**For directory README explanation generation**

- `.\path_explainer.bat /path/to/code -m model_name`

## Demonstration

**Directory comment generation**

https://github.com/user-attachments/assets/e45919ac-2482-4127-8557-151c182ee706

**Directory README explanation generation**

https://github.com/user-attachments/assets/890d5da0-7408-4dd8-ab6d-29047bf96499

## Perfomance comparison

Below are some models that was tested and evaluated.

**Note:**
- Some comparison criteria are subjective, one developer might consider a comment too detailed, while another developer might consider that same comment too oversimplified. 

### Comparison 

Each models were tested with 15 programs. Code Understanding and Comment Quality is **my subjective evaluation**

| Model                     | Code Understanding | Comment Quality | Memory Usage | Limitation                       |
|---------------------------|--------------------|-----------------|--------------|----------------------------------|
| Deepseek-R1:70b           | 4.5                | 5/5             | 42.3 GiB     | Unstable with large files        |
| Codellama:70b             | 0/5                | 0/5             | 38.8 GiB     | Did not understand the prompt    |
| Qwen2.5-coder:32b         | 4.5/5              | 2.5/5           | 21 GiB       |                                  |
| Devstral:24b              | 4/5                | 2/5             | 15.4 GiB     | 200+ lines                       |
| Deepseek-coder-v2:16b     | 4.5/5              | 4.5/5           | 10.4 GiB     | 120+ lines                       |
| Deepseek-R1:8b            | 0/5                | 0/5             | 6.4 GiB      | Did not understand the codes     |
| Web-based Deekseek        | 5/5                | 5/5             | NA           |                                  |
| Web-based ChatGPT         | 4.5/5              | 4/5             | NA           | limited uses with free tier      |

Also compared the performance against 2 popular web-based LLM: Deepseek and ChatGPT.

### Chosen default model

Based on subjective testing, **Deepseek-coder-v2:16b** is chosen as the default model as it strikes a good balance between hardware requirements and overall performance.

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
