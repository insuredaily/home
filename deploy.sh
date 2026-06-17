#!/usr/bin/env bash
set -e

# Terminal colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}     Niche Sites GitHub Pages Deployer         ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed on your system.${NC}"
    exit 1
fi

# Initialize git if not present
if [ ! -d ".git" ]; then
    git init
    git branch -M main
    echo -e "${GREEN}Git repository initialized with branch 'main'.${NC}"
else
    echo -e "Git is already initialized."
fi

# Add gitignore if not present
if [ ! -f ".gitignore" ]; then
    echo "*.pyc" > .gitignore
    echo "__pycache__/" >> .gitignore
    echo "pad_articles.py" >> .gitignore
    echo "patch_sites.py" >> .gitignore
    echo -e "${GREEN}.gitignore created.${NC}"
fi

# Stage all files
git add .

# Check if there is anything to commit
if git diff-index --quiet HEAD --; then
    echo "No modifications to commit."
else
    git commit -m "Finalized 5 monetized websites with proper relative link structures and local assets"
    echo -e "${GREEN}Staged files committed successfully.${NC}"
fi

# Check remote
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || true)
if [ -z "$CURRENT_REMOTE" ]; then
    DEFAULT_REMOTE="https://github.com/insuredaily/home.git"
    echo -e "No git origin remote configured."
    echo -e "Using default target: $DEFAULT_REMOTE"
    git remote add origin "$DEFAULT_REMOTE"
    echo -e "${GREEN}Origin remote set to: $DEFAULT_REMOTE${NC}"
else
    echo -e "Current git origin remote is: $CURRENT_REMOTE"
fi

# Push
echo -e "\n${BLUE}Pushing code to GitHub...${NC}"
git push -u origin main

echo -e "\n${GREEN}===============================================${NC}"
echo -e "${GREEN}🚀 Code successfully pushed to GitHub Pages!${NC}"
echo -e "${GREEN}===============================================${NC}"
