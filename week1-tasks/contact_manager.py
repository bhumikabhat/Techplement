import json
import os
import re
from typing import Dict, List, Optional

class ContactManager:
    def __init__(self, filename: str = "contacts.json"):
        """Initialize the Contact Manager with a JSON file for persistence."""
        self.filename = filename
        self.contacts = self.load_contacts()
    
    def load_contacts(self) -> Dict[str, Dict]:
        """Load contacts from JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    return json.load(file)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading contacts: {e}")
            return {}
    
    def save_contacts(self) -> bool:
        """Save contacts to JSON file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.contacts, file, indent=2)
            return True
        except IOError as e:
            print(f"Error saving contacts: {e}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number (basic validation)."""
        # Remove spaces, dashes, and parentheses
        cleaned_phone = re.sub(r'[\s\-$$$$]', '', phone)
        # Check if it contains only digits and is of reasonable length
        return cleaned_phone.isdigit() and 10 <= len(cleaned_phone) <= 15
    
    def add_contact(self, name: str, phone: str, email: str, address: str = "") -> bool:
        """Add a new contact with validation."""
        try:
            # Validate input
            if not name.strip():
                print("Error: Name cannot be empty.")
                return False
            
            if not phone.strip():
                print("Error: Phone number cannot be empty.")
                return False
            
            if not self.validate_phone(phone):
                print("Error: Invalid phone number format.")
                return False
            
            if email and not self.validate_email(email):
                print("Error: Invalid email format.")
                return False
            
            # Check if contact already exists
            name_key = name.lower().strip()
            if name_key in self.contacts:
                print(f"Error: Contact '{name}' already exists.")
                return False
            
            # Add contact
            self.contacts[name_key] = {
                'name': name.strip(),
                'phone': phone.strip(),
                'email': email.strip(),
                'address': address.strip()
            }
            
            if self.save_contacts():
                print(f"Contact '{name}' added successfully!")
                return True
            else:
                print("Error: Failed to save contact.")
                return False
                
        except Exception as e:
            print(f"Error adding contact: {e}")
            return False
    
    def search_contact(self, search_term: str) -> List[Dict]:
        """Search for contacts by name (partial match)."""
        try:
            search_term = search_term.lower().strip()
            if not search_term:
                print("Error: Search term cannot be empty.")
                return []
            
            results = []
            for key, contact in self.contacts.items():
                if search_term in key or search_term in contact['name'].lower():
                    results.append(contact)
            
            return results
        except Exception as e:
            print(f"Error searching contacts: {e}")
            return []
    
    def update_contact(self, name: str) -> bool:
        """Update an existing contact."""
        try:
            name_key = name.lower().strip()
            if name_key not in self.contacts:
                print(f"Error: Contact '{name}' not found.")
                return False
            
            contact = self.contacts[name_key]
            print(f"\nUpdating contact: {contact['name']}")
            print("Press Enter to keep current value, or type new value:")
            
            # Update name
            new_name = input(f"Name ({contact['name']}): ").strip()
            if new_name:
                # If name is changing, we need to update the key
                if new_name.lower() != name_key:
                    if new_name.lower() in self.contacts:
                        print(f"Error: Contact '{new_name}' already exists.")
                        return False
                    # Remove old key and add new one
                    del self.contacts[name_key]
                    name_key = new_name.lower()
                contact['name'] = new_name
            
            # Update phone
            new_phone = input(f"Phone ({contact['phone']}): ").strip()
            if new_phone:
                if not self.validate_phone(new_phone):
                    print("Error: Invalid phone number format.")
                    return False
                contact['phone'] = new_phone
            
            # Update email
            new_email = input(f"Email ({contact['email']}): ").strip()
            if new_email:
                if not self.validate_email(new_email):
                    print("Error: Invalid email format.")
                    return False
                contact['email'] = new_email
            
            # Update address
            new_address = input(f"Address ({contact['address']}): ").strip()
            if new_address:
                contact['address'] = new_address
            
            # Save updated contact
            self.contacts[name_key] = contact
            
            if self.save_contacts():
                print("Contact updated successfully!")
                return True
            else:
                print("Error: Failed to save updated contact.")
                return False
                
        except Exception as e:
            print(f"Error updating contact: {e}")
            return False
    
    def delete_contact(self, name: str) -> bool:
        """Delete a contact."""
        try:
            name_key = name.lower().strip()
            if name_key not in self.contacts:
                print(f"Error: Contact '{name}' not found.")
                return False
            
            contact_name = self.contacts[name_key]['name']
            confirm = input(f"Are you sure you want to delete '{contact_name}'? (y/N): ").lower()
            
            if confirm == 'y' or confirm == 'yes':
                del self.contacts[name_key]
                if self.save_contacts():
                    print(f"Contact '{contact_name}' deleted successfully!")
                    return True
                else:
                    print("Error: Failed to save changes.")
                    return False
            else:
                print("Deletion cancelled.")
                return False
                
        except Exception as e:
            print(f"Error deleting contact: {e}")
            return False
    
    def list_all_contacts(self) -> None:
        """Display all contacts."""
        try:
            if not self.contacts:
                print("No contacts found.")
                return
            
            print(f"\n{'='*60}")
            print(f"{'ALL CONTACTS':^60}")
            print(f"{'='*60}")
            
            for contact in sorted(self.contacts.values(), key=lambda x: x['name'].lower()):
                self.display_contact(contact)
                print("-" * 60)
                
        except Exception as e:
            print(f"Error listing contacts: {e}")
    
    def display_contact(self, contact: Dict) -> None:
        """Display a single contact in formatted way."""
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email'] if contact['email'] else 'N/A'}")
        print(f"Address: {contact['address'] if contact['address'] else 'N/A'}")
    
    def get_contact_count(self) -> int:
        """Get total number of contacts."""
        return len(self.contacts)


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("     CONTACT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. List All Contacts")
    print("6. Contact Statistics")
    print("7. Exit")
    print("="*50)


def main():
    """Main function to run the Contact Management System."""
    print("Welcome to Contact Management System!")
    print("Developed for Techplement Internship - Week 1 Task")
    
    # Initialize contact manager
    cm = ContactManager()
    
    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                # Add Contact
                print("\n--- ADD NEW CONTACT ---")
                name = input("Enter name: ").strip()
                phone = input("Enter phone number: ").strip()
                email = input("Enter email (optional): ").strip()
                address = input("Enter address (optional): ").strip()
                
                cm.add_contact(name, phone, email, address)
            
            elif choice == '2':
                # Search Contact
                print("\n--- SEARCH CONTACT ---")
                search_term = input("Enter name to search: ").strip()
                results = cm.search_contact(search_term)
                
                if results:
                    print(f"\nFound {len(results)} contact(s):")
                    print("-" * 40)
                    for contact in results:
                        cm.display_contact(contact)
                        print("-" * 40)
                else:
                    print("No contacts found matching your search.")
            
            elif choice == '3':
                # Update Contact
                print("\n--- UPDATE CONTACT ---")
                name = input("Enter name of contact to update: ").strip()
                cm.update_contact(name)
            
            elif choice == '4':
                # Delete Contact
                print("\n--- DELETE CONTACT ---")
                name = input("Enter name of contact to delete: ").strip()
                cm.delete_contact(name)
            
            elif choice == '5':
                # List All Contacts
                cm.list_all_contacts()
            
            elif choice == '6':
                # Contact Statistics
                count = cm.get_contact_count()
                print(f"\n--- CONTACT STATISTICS ---")
                print(f"Total contacts: {count}")
                if count > 0:
                    with_email = sum(1 for contact in cm.contacts.values() if contact['email'])
                    with_address = sum(1 for contact in cm.contacts.values() if contact['address'])
                    print(f"Contacts with email: {with_email}")
                    print(f"Contacts with address: {with_address}")
            
            elif choice == '7':
                # Exit
                print("\nThank you for using Contact Management System!")
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice! Please enter a number between 1-7.")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            print("Thank you for using Contact Management System!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
