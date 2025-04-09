# Folder Structure Generator

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![License](https://img.shields.io/badge/license-MIT-blue)

A Python utility to visualize project directory structures in both text and JSON formats, with optional .gitignore support.

Created by **Adam Suchi Hafizullah** as part of AI-assisted development learning.

## Features

- 📂 Generate clean folder structure visualizations
- ✨ Two output formats: Text (tree) and JSON
- ⚡ Optional .gitignore pattern exclusion
- 🎯 Configurable depth limitation
- 🛠️ Cross-platform (Windows/macOS/Linux)

## Installation

1. Clone the repository or download the script:
```bash
git clone https://github.com/ashafizullah/folder_structure_generator
cd folder-structure-generator
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

## Usage

Run the script with:
```bash
python main.py
```

You'll be prompted for:
1. Project path (leave empty for current directory)
2. Maximum depth (leave empty for unlimited)
3. Whether to exclude files/folders based on .gitignore
4. Output format (text or JSON)

### Example Output Files
* `output.txt` (text tree format)
* `output.json` (structured JSON format)

### Text Output Example
```
Folder Structure for: /projects/my-app
Max Depth: 2
==================================
├── src/
│   ├── components/
│   │   ├── Button.js
│   │   └── Header.js
│   └── App.js
└── package.json
```

### JSON Output Example
```json
{
    "path": "/projects/my-app",
    "max_depth": 2,
    "structure": {
        "src": {
            "components": {
                "Button.js": "file",
                "Header.js": "file"
            },
            "App.js": "file"
        },
        "package.json": "file"
    }
}
```

## Use Cases

1. **Project documentation** - Include structure visualizations in your docs
2. **Code reviews** - Quickly share project layouts
3. **AI training** - Provide context about project structures
4. **Onboarding** - Help new team members understand codebases
5. **Backup planning** - Document important file locations

## Development Notes

This project was created using AI-assisted development techniques, demonstrating:
* Practical Python filesystem operations
* Recursive algorithms
* Clean code architecture
* User-friendly CLI design
* Multiple output format generation

## License

MIT License - Free for personal and commercial use

Created with ❤️ by Adam Suchi Hafizullah