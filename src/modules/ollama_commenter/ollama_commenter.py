import argparse
import requests
import json
import os
import time

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

def check_model_available(model_name):
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        return any(model_name in m for m in models)
    except Exception as e:
        print(f"Model check error: {e}")
        return False

def generate_comments(code, model_name, file_extension):
    """Sends code to Ollama for comment generation."""
    # System prompt to ensure only comments are added
    system_prompt = (
        "You are a code documentation assistant. Your task is to add CLEAR, CONCISE inline comments "
        "to explain the code. Do NOT:\n"
        "1. Modify any existing code\n"
        "2. Add or remove any existing lines of code\n"
        "3. Add comments that state the obvious\n"
        "4. Change code formatting\n"
        "5. Write comments outside code blocks\n"
        "Format rules:\n"
        f"- For .{file_extension} files: Use appropriate comment syntax\n"
        "- Place comments ABOVE relevant lines\n"
        "- Be professional and technical\n"
        "6. Repeat, it is extremely important that you do not change, add or remove any code"
    )
    
    prompt = f"Add inline comments to this {file_extension.upper()} code without changing any code:\n\n{code}"
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Ollama API error: {e}")
        exit(1)

def save_output(original_path, commented_code):
    base_name = os.path.splitext(original_path)[0]
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = f"{base_name}_commented_{timestamp}{os.path.splitext(original_path)[1]}"
    try:
        with open(output_path, 'w') as file:
            file.write(commented_code)
        print(f"Success! Commented code saved to: {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Code Commenter using Ollama")
    parser.add_argument("file", help="Path to code file (.c, .py, .js, .java, etc.)")
    parser.add_argument("-m", "--model", default="deepseek-coder-v2:16b", 
                        help="Ollama model name (default: deepseek-coder-v2:16b)")
    
    args = parser.parse_args()
    
    if not check_model_available(args.model):
        print(f"Model '{args.model}' not found. Install with: ollama pull {args.model}")
        exit(1)

    if not os.path.exists(args.file):
        print(f"Error: File not found - {args.file}")
        exit(1)
    
    file_ext = os.path.splitext(args.file)[1][1:]
    
    code = read_file(args.file)
    
    print("Generating comments... (This may take a moment)")
    commented_code = generate_comments(code, args.model, file_ext)
    
    save_output(args.file, commented_code)

if __name__ == "__main__":
    main()