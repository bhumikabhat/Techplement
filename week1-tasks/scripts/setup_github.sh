#!/bin/bash

# GitHub Setup Script for Techplement Internship
echo "🚀 Setting up GitHub repository for Techplement internship..."

# Check if we're in the right directory
if [ ! -f "contact_manager.py" ]; then
    echo "❌ Error: contact_manager.py not found. Please run this script from the week1-tasks directory."
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Week 1 Task: Contact Management System - Python

Features:
- Add, search, update, delete contacts
- Data validation and error handling
- JSON file persistence
- Command-line interface
- Comprehensive documentation

Completed for Techplement Internship Program"

echo "✅ Local Git setup complete!"
echo ""
echo "🔗 Next steps:"
echo "1. Go to https://github.com and create a new repository named 'Techplement'"
echo "2. Run these commands to push your code:"
echo "   git remote add origin https://github.com/YOURUSERNAME/Techplement.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Don't forget to:"
echo "   - Post on LinkedIn with #techplement hashtags"
echo "   - Add internship experience to LinkedIn"
echo "   - Join the Telegram and WhatsApp channels"
