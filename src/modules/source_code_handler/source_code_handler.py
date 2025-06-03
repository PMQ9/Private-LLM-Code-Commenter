import os
import ast
import re

def find_source_files(directory, extensions=['.py', '.c', '.sh']):
    """Find all files with specified extensions in the directory."""
    source_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                source_files.append(os.path.join(root, file))
    return source_files

def process_file(file_path, model_name):
    """Process a single file based on its extension."""
    with open(file_path, 'r') as f:
        content = f.read()

    if file_path.endswith('.py'):
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
                func_code = content.splitlines()[node.lineno-1:node.body[0].lineno]
                prompt = f"Generate a docstring description for this function:\n{''.join(func_code)}"
                docstring = get_llm_response(prompt, model_name)
                # Insert docstring logic here (simplified for brevity)
    
    elif file_path.endswith('.c'):
        functions = re.findall(r'^\w+\s+\w+\s*\([^)]*\)\s*{[^}]*}', content, re.MULTILINE)
        for func in functions:
            prompt = f"Generate a comment for this function:\n{func}"
            comment = get_llm_response(prompt, model_name)
            # Insert comment above function logic here
    
    elif file_path.endswith('.sh'):
        functions = re.findall(r'^\w+\s*\(\)\s*{[^}]*}', content, re.MULTILINE)
        for func in functions:
            prompt = f"Generate a comment for this shell function:\n{func}"
            comment = get_llm_response(prompt, model_name)
            # Insert comment above function logic here

# Example usage
directory = "./my_project"
model = "deepseek-coder-v2"
files = find_source_files(directory)
for file in files:
    process_file(file, model)