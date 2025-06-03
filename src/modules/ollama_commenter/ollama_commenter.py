import os
import argparse
import ollama
from pathlib import Path
import mimetypes

def is_text_file(filepath):
    """Check if a file is text-based using mimetypes and extension."""
    # First check by mimetype
    mime = mimetypes.guess_type(filepath)[0]
    if mime and mime.startswith('text/'):
        return True
    
    # Check common source file extensions
    source_extensions = {'.c', '.h', '.cpp', '.hpp', '.py', '.java', 
                         '.js', '.ts', '.html', '.css', '.php', '.rb',
                         '.go', '.rs', '.swift', '.kt', '.m', '.cs', 
                         '.sh', '.pl', '.lua', '.sql', '.json', '.xml'}
    return Path(filepath).suffix.lower() in source_extensions

def process_with_ollama(content, model="devtral"):
    """Send content to local Ollama for commenting using the Python library."""
    prompt = (
        "Add detailed comments to explain this code. "
        "Do NOT modify any existing code. Only add comments. "
        "Preserve all original formatting exactly. "
        "Output ONLY the commented code with no additional text:\n\n"
        f"{content}"
    )
    
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={'temperature': 0.1}
        )
        return response['response'].strip()
    except Exception as e:
        print(f"Ollama processing error: {e}")
        return content

def chunk_file(content, max_chars=3000):
    """Split content into chunks respecting line boundaries."""
    chunks = []
    current_chunk = []
    current_length = 0

    for line in content.splitlines(keepends=True):
        line_length = len(line)
        if current_length + line_length > max_chars and current_chunk:
            chunks.append(''.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(line)
        current_length += line_length

    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks

def process_file(filepath, model="devtral"):
    """Process a single file through Ollama for commenting."""
    print(f"Processing: {filepath}")
    
    # Read file content
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"  Warning: Binary file detected. Skipping {filepath}")
        return None

    # Process in chunks if needed
    chunks = chunk_file(content) if len(content) > 3000 else [content]
    processed_chunks = []

    for i, chunk in enumerate(chunks, 1):
        print(f"  Processing chunk {i}/{len(chunks)}")
        processed_chunks.append(process_with_ollama(chunk, model))

    result = ''.join(processed_chunks)

    # Write output
    output_path = filepath.with_suffix(filepath.suffix + '.commented')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  Created: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Add comments to source files using Ollama')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('--model', default='devtral', help='Ollama model to use')
    parser.add_argument('--ext', action='append', help='Additional file extensions to process')
    args = parser.parse_args()

    # Supported file extensions
    extensions = {
        '.c', '.h', '.cpp', '.hpp', '.py', '.java', 
        '.js', '.ts', '.html', '.css', '.php', '.rb',
        '.go', '.rs', '.swift', '.kt', '.m', '.cs'
    }
    
    # Add custom extensions if provided
    if args.ext:
        for ext in args.ext:
            extensions.add(ext.lower())

    processed_files = []
    for root, _, files in os.walk(args.directory):
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in extensions and is_text_file(path):
                try:
                    output = process_file(path, args.model)
                    if output:
                        processed_files.append((path, output))
                except Exception as e:
                    print(f"Failed to process {path}: {str(e)}")

    print("\nProcessing complete. Modified files:")
    for original, modified in processed_files:
        print(f"  {original} -> {modified}")

if __name__ == "__main__":
    mimetypes.init()  # Initialize MIME type database
    main()