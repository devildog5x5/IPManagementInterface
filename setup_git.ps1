# Git Setup Script for IP Device Management Interface
# This script initializes the Git repository and makes the initial commit

Write-Host "Setting up Git repository..." -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Initialize repository if not already initialized
if (-not (Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "Git repository already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Making initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: IP Device Management Interface
    
    - Main application with GUI (Tkinter)
    - IP device management (CRUD operations)
    - Network tools (ping, port scanner, network info)
    - Data persistence (JSON storage)
    - Installer script and requirements
    - Documentation and README"
    
    Write-Host "Initial commit completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To connect to a remote repository:" -ForegroundColor Cyan
    Write-Host "  git remote add origin <repository-url>" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor Cyan
} else {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Git setup complete!" -ForegroundColor Green

