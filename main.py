import os
import json
import re
from pathlib import Path
from typing import Dict, List, Union

def parse_gitignore(gitignore_path: str) -> List[str]:
    """Parse .gitignore file and return patterns to exclude"""
    exclude_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('/'):
                        line = line[1:]
                    if line.endswith('/'):
                        line = line[:-1]
                    exclude_patterns.append(line)
    return exclude_patterns

def should_exclude(path: str, exclude_patterns: List[str], root_path: str) -> bool:
    """Check if path should be excluded based on .gitignore patterns"""
    rel_path = os.path.relpath(path, root_path).replace('\\', '/')
    
    for pattern in exclude_patterns:
        if pattern.endswith('*'):
            if rel_path.startswith(pattern[:-1]):
                return True
        elif rel_path == pattern:
            return True
        elif f"{rel_path}/".startswith(f"{pattern}/"):
            return True
        elif '*' in pattern:
            if re.match(pattern.replace('*', '.*'), rel_path):
                return True
    return False

def generate_text_structure(startpath: str, output_file, max_depth: int = None, 
                          current_depth: int = 0, exclude_patterns: List[str] = None, 
                          root_path: str = None):
    """Generate folder structure in text format"""
    if max_depth is not None and current_depth > max_depth:
        return
    
    if root_path is None:
        root_path = startpath
    
    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        return
    
    entries = [e for e in entries if not e.startswith('.') or e == '.gitignore']
    
    for i, entry in enumerate(entries):
        full_path = os.path.join(startpath, entry)
        
        if exclude_patterns and should_exclude(full_path, exclude_patterns, root_path):
            continue
            
        indent = '    ' * current_depth
        is_last = i == len(entries) - 1
        
        if os.path.isdir(full_path):
            output_file.write(f"{indent}{'└── ' if is_last else '├── '}{entry}/\n")
            generate_text_structure(
                full_path, output_file, max_depth, current_depth + 1,
                exclude_patterns, root_path
            )
        else:
            output_file.write(f"{indent}{'└── ' if is_last else '├── '}{entry}\n")

def generate_json_structure(startpath: str, max_depth: int = None, 
                          current_depth: int = 0, exclude_patterns: List[str] = None,
                          root_path: str = None) -> Union[Dict, str]:
    """Generate folder structure in JSON format"""
    if max_depth is not None and current_depth > max_depth:
        return None
    
    if root_path is None:
        root_path = startpath
    
    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        return None
    
    entries = [e for e in entries if not e.startswith('.') or e == '.gitignore']
    
    structure = {}
    for entry in entries:
        full_path = os.path.join(startpath, entry)
        
        if exclude_patterns and should_exclude(full_path, exclude_patterns, root_path):
            continue
            
        if os.path.isdir(full_path):
            children = generate_json_structure(
                full_path, max_depth, current_depth + 1,
                exclude_patterns, root_path
            )
            if children is not None:
                structure[entry] = children
        else:
            structure[entry] = "file"
    
    return structure if structure else None

def main():
    print("Folder Structure Generator")
    print("-------------------------")
    
    # Get project path
    project_path = input("Enter project path (leave empty for current directory): ").strip()
    if not project_path:
        project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print("Error: Path does not exist!")
        return
    
    # Get max depth
    max_depth_input = input("Enter max depth (leave empty for unlimited): ").strip()
    try:
        max_depth = int(max_depth_input) if max_depth_input else None
    except ValueError:
        print("Invalid depth value. Using unlimited depth.")
        max_depth = None
    
    # .gitignore support (silent mode - won't show in output)
    use_gitignore = input("Exclude files/folders based on .gitignore? (y/n): ").strip().lower() == 'y'
    exclude_patterns = []
    
    if use_gitignore:
        gitignore_path = os.path.join(project_path, '.gitignore')
        exclude_patterns = parse_gitignore(gitignore_path)
    
    # Output format selection
    output_format = input("Select output format (text/json): ").strip().lower()
    while output_format not in ['text', 'json']:
        print("Invalid format. Please choose 'text' or 'json'")
        output_format = input("Select output format (text/json): ").strip().lower()
    
    # Output file path
    output_path = os.path.join(os.getcwd(), f"output.{'txt' if output_format == 'text' else 'json'}")
    
    try:
        if output_format == 'text':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Folder Structure for: {project_path}\n")
                f.write(f"Max Depth: {'Unlimited' if max_depth is None else max_depth}\n")
                f.write("=" * 50 + "\n\n")
                generate_text_structure(
                    project_path, f, max_depth,
                    exclude_patterns=exclude_patterns,
                    root_path=project_path
                )
        else:
            structure = generate_json_structure(
                project_path, max_depth,
                exclude_patterns=exclude_patterns,
                root_path=project_path
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "path": project_path,
                    "max_depth": max_depth,
                    "structure": structure
                }, f, indent=4)
        
        print(f"\nSuccess! Folder structure saved to {output_path}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()