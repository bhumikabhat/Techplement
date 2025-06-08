"""
Test script for Contact Management System
This file contains basic tests to verify the functionality
"""

from contact_manager import ContactManager
import os
import json

def test_contact_manager():
    """Basic test function for ContactManager"""
    print("Running basic tests for Contact Management System...")
    
    # Create a test instance with a different filename
    test_cm = ContactManager("test_contacts.json")
    
    # Test 1: Add contact
    print("\nTest 1: Adding a contact")
    result = test_cm.add_contact("Test User", "1234567890", "test@example.com", "Test Address")
    assert result == True, "Failed to add contact"
    print("✓ Contact added successfully")
    
    # Test 2: Search contact
    print("\nTest 2: Searching for contact")
    results = test_cm.search_contact("Test")
    assert len(results) == 1, "Failed to find contact"
    assert results[0]['name'] == "Test User", "Wrong contact found"
    print("✓ Contact found successfully")
    
    # Test 3: Validate email
    print("\nTest 3: Email validation")
    assert test_cm.validate_email("test@example.com") == True, "Valid email rejected"
    assert test_cm.validate_email("invalid-email") == False, "Invalid email accepted"
    print("✓ Email validation working correctly")
    
    # Test 4: Validate phone
    print("\nTest 4: Phone validation")
    assert test_cm.validate_phone("1234567890") == True, "Valid phone rejected"
    assert test_cm.validate_phone("123") == False, "Invalid phone accepted"
    print("✓ Phone validation working correctly")
    
    # Test 5: Contact count
    print("\nTest 5: Contact count")
    count = test_cm.get_contact_count()
    assert count == 1, f"Expected 1 contact, got {count}"
    print("✓ Contact count correct")
    
    # Cleanup test file
    if os.path.exists("test_contacts.json"):
        os.remove("test_contacts.json")
    
    print("\n🎉 All tests passed successfully!")
    print("Contact Management System is working correctly.")

if __name__ == "__main__":
    test_contact_manager()
