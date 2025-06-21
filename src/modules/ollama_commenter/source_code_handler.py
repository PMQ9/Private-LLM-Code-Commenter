import os
import subprocess
import argparse

def find_source_files(root_dir, extensions):
    """
    Recursively find all files in root_dir and its subdirectories
    that have the specified extensions.
    """
    source_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                source_files.append(os.path.join(dirpath, filename))
    return source_files

def main():
    parser = argparse.ArgumentParser(description="Batch process source files with ollama_commenter.py")
    parser.add_argument("root_dir", help="Root directory to search for source files")
    parser.add_argument("-e", "--extensions", nargs='+', default=['.py', '.c', '.cpp', '.java', '.js'],
                        help="List of file extensions to process (e.g., .py .js)")
    parser.add_argument("-s", "--script", default="ollama_commenter.py",
                        help="Path to ollama_commenter.py script")
    
    args = parser.parse_args()
    
    # Find all source files with the specified extensions
    source_files = find_source_files(args.root_dir, args.extensions)
    
    if not source_files:
        print("No source files found with the specified extensions.")
        return
    
    print(f"Found {len(source_files)} source files to process.")
    
    for file in source_files:
        print(f"Processing {file}...")
        try:
            # Call ollama_commenter.py with the file as argument
            subprocess.run(["python", args.script, file], check=True)
            print(f"Successfully processed {file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {file}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {file}: {e}")

if __name__ == "__main__":
    main()