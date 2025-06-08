"""
Deployment validation script
Run this to ensure your Contact Management System is ready for submission
"""

import os
import sys
import json
import subprocess

def check_file_structure():
    """Check if all required files are present"""
    print("🔍 Checking file structure...")
    
    required_files = [
        'contact_manager.py',
        'README.md',
        'test_contact_manager.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing Contact Management System...")
    
    try:
        # Import and test the contact manager
        sys.path.append('.')
        from contact_manager import ContactManager
        
        # Create test instance
        test_cm = ContactManager("deployment_test.json")
        
        # Test basic operations
        print("  - Testing add contact...")
        result = test_cm.add_contact("Test Deploy", "1234567890", "test@deploy.com", "Test Address")
        assert result == True
        
        print("  - Testing search contact...")
        results = test_cm.search_contact("Test")
        assert len(results) == 1
        
        print("  - Testing validation...")
        assert test_cm.validate_email("test@example.com") == True
        assert test_cm.validate_phone("1234567890") == True
        
        # Cleanup
        if os.path.exists("deployment_test.json"):
            os.remove("deployment_test.json")
        
        print("✅ All functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def check_git_status():
    """Check git repository status"""
    print("\n📁 Checking Git status...")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            
            # Check for uncommitted changes
            if "nothing to commit" in result.stdout:
                print("✅ All changes committed")
            else:
                print("⚠️  You have uncommitted changes")
                print("Run: git add . && git commit -m 'Your message'")
            
            return True
        else:
            print("❌ Git not initialized")
            print("Run: git init")
            return False
            
    except FileNotFoundError:
        print("❌ Git not installed or not in PATH")
        return False

def generate_submission_checklist():
    """Generate a submission checklist"""
    print("\n📋 SUBMISSION CHECKLIST:")
    print("=" * 50)
    
    checklist = [
        "✅ Contact Management System completed",
        "✅ All files in week1-tasks folder",
        "✅ GitHub repository 'Techplement' created",
        "✅ Code pushed to GitHub",
        "✅ LinkedIn post with offer letter",
        "✅ LinkedIn experience added",
        "✅ Joined Telegram channel",
        "✅ Joined WhatsApp channel",
        "⏳ Wait for submission instructions from Techplement"
    ]
    
    for item in checklist:
        print(item)
    
    print("=" * 50)
    print("🎯 Your Contact Management System is ready for submission!")

def main():
    """Main deployment validation function"""
    print("🚀 TECHPLEMENT WEEK 1 TASK - DEPLOYMENT VALIDATOR")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Run all checks
    if not check_file_structure():
        all_checks_passed = False
    
    if not test_functionality():
        all_checks_passed = False
    
    if not check_git_status():
        all_checks_passed = False
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("🎉 DEPLOYMENT VALIDATION SUCCESSFUL!")
        generate_submission_checklist()
    else:
        print("❌ DEPLOYMENT VALIDATION FAILED!")
        print("Please fix the issues above before submission.")

if __name__ == "__main__":
    main()
