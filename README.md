# Python Project Analyzer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![License](https://img.shields.io/badge/license-MIT-blue)

A powerful Python utility that helps developers and AI assistants better understand codebases by visualizing project structures and combining code files with smart filtering options.

Created by **Adam Suchi Hafizullah** as part of AI-assisted development learning.

## 🚀 Key Features

- **Dual-Format Structure Visualization**
  - 📋 Text Format (Tree View) - Human-readable directory structure
  - 🔄 JSON Format - Machine-processable structure for integrations
  
- **Smart Code Concatenator**
  - 📦 Combines all code files from any directory
  - 🏷️ Adds clear file boundaries with descriptive headers
  - 🔠 Supports 30+ programming languages
  
- **Intelligent Filtering**
  - 🚫 .gitignore-aware scanning
  - 🔍 Configurable depth limitation for large projects
  - 📊 Detailed processing summaries

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/ashafizullah/folder_structure_generator
cd folder_structure_generator
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

3. No additional dependencies required - uses Python standard library only!

## 📋 Usage

Run the script:
```bash
python main.py
```

### Interactive Menu Options:

**1. Generate Folder Structure**
   - Choose between Text and JSON formats
   - Specify project path (defaults to current directory)
   - Set maximum depth (optional)
   - Enable .gitignore pattern exclusion

**2. Concatenate Code Files**
   - Select target folder to analyze
   - Automatically detects supported code files
   - Apply .gitignore filtering (optional)
   - Creates a single document with all code files

**3. Exit**

## 📄 Output Files

The tool generates the following output files:

- **Text Format**: `folder_structure.txt` - A tree-like representation of your project
- **JSON Format**: `folder_structure.json` - A structured data representation
- **Code Concatenation**: `combined_code.txt` - All code files combined with clear separators

## 🎯 Use Cases

1. **Project Documentation**
   - Include structure visualizations in your documentation
   - Create snapshots of project evolution over time

2. **AI Context Generation**
   - Feed project structure to AI tools for better code suggestions
   - Help AI assistants understand your codebase at a glance

3. **Onboarding and Knowledge Transfer**
   - Help new team members quickly grasp project organization
   - Create code inventories for handover documentation

4. **Code Reviews**
   - Share complete project context with reviewers
   - Highlight structural changes between versions

5. **Legacy Code Analysis**
   - Quickly map unfamiliar codebases
   - Identify code organization patterns

## 🧠 Technical Details

The analyzer uses several key techniques:

- **Recursive Directory Traversal** - For efficient folder scanning
- **Gitignore Pattern Matching** - For intelligent file filtering
- **File Extension Detection** - For identifying code files
- **Unicode-Safe File Handling** - For cross-platform compatibility
- **JSON Serialization** - For structured data output

## 🤝 Contributing

Contributions are welcome! Here are ways you can help:

1. Add support for more code file extensions
2. Improve gitignore pattern matching
3. Add export options (e.g., XML, HTML visualization)
4. Create unit tests

## 📜 License

MIT License - Free for personal and commercial use

---

Created with ❤️ by Adam Suchi Hafizullah

*This project demonstrates practical Python filesystem operations, recursive algorithms, and AI-assisted development techniques.*