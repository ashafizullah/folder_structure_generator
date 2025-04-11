import os
import json
import re
from pathlib import Path

def parse_gitignore(gitignore_path):
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

def should_exclude(path, exclude_patterns, root_path):
    """Check if path should be excluded based on patterns"""
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

def generate_text_structure(startpath, output_file, max_depth=None, current_depth=0, exclude_patterns=None, root_path=None):
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
                full_path, output_file, max_depth, 
                current_depth + 1, exclude_patterns, root_path
            )
        else:
            output_file.write(f"{indent}{'└── ' if is_last else '├── '}{entry}\n")

def generate_json_structure(startpath, max_depth=None, current_depth=0, exclude_patterns=None, root_path=None):
    """Generate folder structure in JSON format"""
    if max_depth is not None and current_depth > max_depth:
        return {}
    
    if root_path is None:
        root_path = startpath
    
    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        return {}
    
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
            if children:
                structure[entry] = children
        else:
            structure[entry] = None
    
    return structure

def concatenate_code_files(folder_path, output_file, exclude_patterns=None):
    """Concatenate all code files from a folder with separators"""
    CODE_EXTENSIONS = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.kt', '.cpp', '.c', '.h', 
        '.hpp', '.cs', '.go', '.rb', '.php', '.swift', '.m', '.mm', '.dart',
        '.rs', '.sh', '.pl', '.lua', '.r', '.scala', '.groovy', '.f', '.for',
        '.f90', '.html', '.css', '.scss', '.less', '.sass', '.vue', '.elm'
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            file_count = 0
            skipped_files = 0
            error_files = 0
            
            print(f"\nScanning folder: {folder_path}")
            
            for root, _, files in os.walk(folder_path):
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, folder_path)
                    
                    if exclude_patterns and should_exclude(file_path, exclude_patterns, folder_path):
                        print(f"Skipping excluded: {rel_path}")
                        skipped_files += 1
                        continue
                    
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    
                    if ext not in CODE_EXTENSIONS:
                        skipped_files += 1
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as in_f:
                            out_f.write(f"\n{'=' * 80}\n")
                            out_f.write(f"FILE: {rel_path}\n")
                            out_f.write(f"{'=' * 80}\n\n")
                            out_f.write(in_f.read())
                            out_f.write("\n")
                            
                            file_count += 1
                            print(f"Processed: {rel_path}")
                            
                    except PermissionError:
                        print(f"Permission denied: {rel_path}")
                        error_files += 1
                    except Exception as e:
                        print(f"Error processing {rel_path}: {str(e)}")
                        error_files += 1
            
            print(f"\n{'=' * 50}")
            print("Processing Summary:")
            print(f"Files processed successfully: {file_count}")
            print(f"Files skipped (non-code): {skipped_files}")
            print(f"Files with errors: {error_files}")
            print(f"Output saved to: {os.path.abspath(output_file)}")
            print(f"{'=' * 50}")
                        
    except Exception as e:
        print(f"\nError writing output: {str(e)}")

def main_menu():
    print("\n" + "=" * 50)
    print("PYTHON PROJECT ANALYZER")
    print("=" * 50)
    print("1. Generate Folder Structure")
    print("2. Concatenate Code Files from Folder")
    print("3. Exit")
    return input("Select option (1-3): ").strip()

def folder_structure_menu():
    print("\n" + "=" * 50)
    print("FOLDER STRUCTURE GENERATOR")
    print("=" * 50)
    print("1. Text Format (Tree)")
    print("2. JSON Format")
    print("3. Back to Main Menu")
    return input("Select output format (1-3): ").strip()

def main():
    while True:
        choice = main_menu()
        
        if choice == '1':
            while True:
                format_choice = folder_structure_menu()
                
                if format_choice == '1' or format_choice == '2':
                    print("\nFolder Structure Generator")
                    print("-" * 50)
                    
                    project_path = input("Enter project path (leave empty for current directory): ").strip()
                    if not project_path:
                        project_path = os.getcwd()
                    
                    if not os.path.exists(project_path):
                        print("Error: Path does not exist!")
                        continue
                    
                    max_depth_input = input("Enter max depth (leave empty for unlimited): ").strip()
                    try:
                        max_depth = int(max_depth_input) if max_depth_input else None
                    except ValueError:
                        print("Invalid depth value. Using unlimited depth.")
                        max_depth = None
                    
                    use_gitignore = input("Exclude files/folders based on .gitignore? (y/n): ").strip().lower() == 'y'
                    exclude_patterns = []
                    
                    if use_gitignore:
                        gitignore_path = os.path.join(project_path, '.gitignore')
                        exclude_patterns = parse_gitignore(gitignore_path)
                    
                    if format_choice == '1':
                        output_path = os.path.join(os.getcwd(), "folder_structure.txt")
                        try:
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(f"Folder Structure for: {project_path}\n")
                                f.write(f"Max Depth: {'Unlimited' if max_depth is None else max_depth}\n")
                                f.write("=" * 50 + "\n\n")
                                generate_text_structure(
                                    project_path, f, max_depth,
                                    exclude_patterns=exclude_patterns,
                                    root_path=project_path
                                )
                            print(f"\nSuccess! Folder structure saved to {output_path}")
                        except Exception as e:
                            print(f"Error occurred: {str(e)}")
                    
                    elif format_choice == '2':
                        output_path = os.path.join(os.getcwd(), "folder_structure.json")
                        try:
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
                            print(f"\nSuccess! JSON structure saved to {output_path}")
                        except Exception as e:
                            print(f"Error occurred: {str(e)}")
                    
                elif format_choice == '3':
                    break
                else:
                    print("Invalid option. Please try again.")
                
                input("\nPress Enter to continue...")
                
        elif choice == '2':
            print("\nCode File Concatenator")
            print("-" * 50)
            
            folder_path = input("Enter folder path to scan for code files: ").strip()
            if not folder_path:
                folder_path = os.getcwd()
            
            if not os.path.exists(folder_path):
                print("Error: Path does not exist!")
                continue
            
            use_gitignore = input("Exclude files/folders based on .gitignore? (y/n): ").strip().lower() == 'y'
            exclude_patterns = []
            
            if use_gitignore:
                gitignore_path = os.path.join(folder_path, '.gitignore')
                exclude_patterns = parse_gitignore(gitignore_path)
            
            output_path = os.path.join(os.getcwd(), "combined_code.txt")
            
            concatenate_code_files(folder_path, output_path, exclude_patterns)
            
        elif choice == '3':
            print("Exiting program...")
            break
            
        else:
            print("Invalid option. Please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()