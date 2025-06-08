# Contact Management System

A command-line contact management system built with Python for Techplement Internship Week 1 Task.

## Features

- **Add Contacts**: Add new contacts with name, phone, email, and address
- **Search Contacts**: Search for contacts by name (supports partial matching)
- **Update Contacts**: Modify existing contact information
- **Delete Contacts**: Remove contacts with confirmation
- **List All Contacts**: Display all contacts in a formatted view
- **Data Persistence**: Contacts are saved to and loaded from a JSON file
- **Data Validation**: Email and phone number validation
- **Error Handling**: Comprehensive error handling throughout the application

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only built-in Python modules)

## Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/Techplement.git
cd Techplement/week1-tasks
\`\`\`

2. Run the application:
\`\`\`bash
python contact_manager.py
\`\`\`

## Usage

### Running the Application

Execute the main script:
\`\`\`bash
python contact_manager.py
\`\`\`

### Menu Options

1. **Add Contact**: Enter contact details including name, phone, email, and address
2. **Search Contact**: Find contacts by entering a name or partial name
3. **Update Contact**: Modify existing contact information
4. **Delete Contact**: Remove a contact from the system
5. **List All Contacts**: View all stored contacts
6. **Contact Statistics**: View summary information about your contacts
7. **Exit**: Close the application

### Data Storage

Contacts are automatically saved to `contacts.json` in the same directory as the script. The file is created automatically when you add your first contact.

## Validation Rules

- **Name**: Cannot be empty
- **Phone**: Must contain only digits (with optional formatting characters) and be 10-15 digits long
- **Email**: Must follow standard email format (optional field)
- **Address**: Optional field

## Error Handling

The application includes comprehensive error handling for:
- Invalid input data
- File I/O operations
- Duplicate contact names
- Missing contacts during search/update/delete operations
- JSON parsing errors

## File Structure

\`\`\`
week1-tasks/
├── contact_manager.py    # Main application file
├── README.md            # This documentation
└── contacts.json        # Data storage (created automatically)
\`\`\`

## Example Usage

\`\`\`
Welcome to Contact Management System!
Developed for Techplement Internship - Week 1 Task

==================================================
     CONTACT MANAGEMENT SYSTEM
==================================================
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. List All Contacts
6. Contact Statistics
7. Exit
==================================================
Enter your choice (1-7): 1

--- ADD NEW CONTACT ---
Enter name: John Doe
Enter phone number: 1234567890
Enter email (optional): john.doe@email.com
Enter address (optional): 123 Main St, City
Contact 'John Doe' added successfully!
\`\`\`

## Technical Details

- **Language**: Python 3.6+
- **Data Structure**: Dictionary for in-memory storage
- **Persistence**: JSON file format
- **Validation**: Regular expressions for email and phone validation
- **Architecture**: Object-oriented design with ContactManager class

## Author

Created for Techplement Internship Program - Week 1 Task

## License

This project is created for educational purposes as part of an internship program.
