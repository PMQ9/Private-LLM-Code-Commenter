import os
import argparse
import requests
import json
import sys
from tqdm import tqdm

# Mapping of file extensions to programming languages
extension_to_language = {
    '.py': 'Python',
    '.c': 'C',
    '.cpp': 'C++',
    '.java': 'Java',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.go': 'Go',
    '.rb': 'Ruby',
}

def find_source_files(root_dir, extensions):
    """Recursively find all files in root_dir with the specified extensions."""
    source_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                source_files.append(os.path.abspath(os.path.join(dirpath, filename)))
    return source_files

def check_ollama_available():
    """Check if the Ollama server is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def check_model_available(model_name):
    """Check if the specified model is available in Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        return any(model_name in m for m in models)
    except requests.exceptions.RequestException:
        return False

def generate_explanation(code, model_name, language):
    """Generate an explanation of the code using Ollama."""
    system_prompt = (
        "You are a code analyst. Your task is to provide a very brief explanation of what the following code does. "
        "Focus on the main functionality and purpose of the code. Again, very brief."
    )
    prompt = f"Explain what this {language} code does:\n\n{code}"
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.5}
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
        print(f"Ollama API error: {e}", file=sys.stderr)
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate explanations for source code files using Ollama")
    parser.add_argument("root_dir", help="Root directory to search for source files")
    parser.add_argument("-e", "--extensions", nargs='+', default=['.py', '.c', '.cpp', '.java', '.js'],
                        help="List of file extensions to process (e.g., .py .js)")
    parser.add_argument("-m", "--model", default="deepseek-coder-v2:16b",
                        help="Ollama model name (default: deepseek-coder-v2:16b)")
    parser.add_argument("-o", "--output", default="code_explanations.md",
                        help="Output file name (default: code_explanations.md)")
    
    args = parser.parse_args()
    
    # Check if Ollama server and model are available
    if not check_ollama_available():
        print("Ollama server is not running. Please start it with 'ollama serve'.")
        exit(1)
    
    if not check_model_available(args.model):
        print(f"Model '{args.model}' is not available. Please pull it with 'ollama pull {args.model}'.")
        exit(1)
    
    # Find source files
    source_files = find_source_files(args.root_dir, args.extensions)
    
    if not source_files:
        print("No source files found with the specified extensions.")
        return
    
    print(f"Found {len(source_files)} source files to process.")
    
    explanations = []
    
    # Process each source file
    for file in tqdm(source_files, desc="Processing files"):
        ext = os.path.splitext(file)[1]
        if ext not in extension_to_language:
            print(f"Skipping {file}: unknown extension {ext}")
            continue
        language = extension_to_language[ext]
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
        explanation = generate_explanation(code, args.model, language)
        if explanation is not None:
            rel_path = os.path.relpath(file, args.root_dir)
            explanations.append((rel_path, explanation))
        else:
            print(f"Failed to generate explanation for {file}")
    
    # Write explanations to output file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("# Code Explanations\n\n")
            for rel_path, explanation in explanations:
                f.write(f"## {rel_path}\n{explanation}\n\n")
        print(f"Explanations written to {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        exit(1)

if __name__ == "__main__":
    main()