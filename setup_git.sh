#!/bin/bash
# Git Setup Script for IP Device Management Interface
# This script initializes the Git repository and makes the initial commit

echo "Setting up Git repository..."

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed or not in PATH"
    echo "Please install Git from https://git-scm.com/downloads"
    exit 1
fi

echo "Git found: $(git --version)"

# Initialize repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
else
    echo "Git repository already initialized"
fi

# Add all files
echo "Adding files to Git..."
git add .

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo "Making initial commit..."
    git commit -m "Initial commit: IP Device Management Interface

- Main application with GUI (Tkinter)
- IP device management (CRUD operations)
- Network tools (ping, port scanner, network info)
- Data persistence (JSON storage)
- Installer script and requirements
- Documentation and README"
    
    echo "Initial commit completed successfully!"
    echo ""
    echo "To connect to a remote repository:"
    echo "  git remote add origin <repository-url>"
    echo "  git push -u origin main"
else
    echo "No changes to commit"
fi

echo ""
echo "Git setup complete!"

