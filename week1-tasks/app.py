from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    return json.load(file)
            return {}
        except (json.JSONDecodeError, IOError):
            return {}
    
    def save_contacts(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.contacts, file, indent=2)
            return True
        except IOError:
            return False
    
    def validate_email(self, email):
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        cleaned_phone = re.sub(r'[\s\-()]', '', phone)
        return cleaned_phone.isdigit() and 10 <= len(cleaned_phone) <= 15
    
    def add_contact(self, name, phone, email="", address=""):
        name_key = name.lower().strip()
        if name_key in self.contacts:
            return False, "Contact already exists"
        
        if not self.validate_phone(phone):
            return False, "Invalid phone number"
        
        if email and not self.validate_email(email):
            return False, "Invalid email format"
        
        self.contacts[name_key] = {
            'name': name.strip(),
            'phone': phone.strip(),
            'email': email.strip(),
            'address': address.strip(),
            'created_at': datetime.now().isoformat()
        }
        
        if self.save_contacts():
            return True, "Contact added successfully"
        return False, "Failed to save contact"
    
    def search_contacts(self, search_term):
        if not search_term:
            return list(self.contacts.values())
        
        search_term = search_term.lower()
        results = []
        for contact in self.contacts.values():
            if (search_term in contact['name'].lower() or 
                search_term in contact['phone'] or 
                search_term in contact['email'].lower()):
                results.append(contact)
        return results
    
    def get_contact(self, name):
        name_key = name.lower().strip()
        return self.contacts.get(name_key)
    
    def update_contact(self, old_name, name, phone, email="", address=""):
        old_key = old_name.lower().strip()
        if old_key not in self.contacts:
            return False, "Contact not found"
        
        if not self.validate_phone(phone):
            return False, "Invalid phone number"
        
        if email and not self.validate_email(email):
            return False, "Invalid email format"
        
        # If name changed, check if new name already exists
        new_key = name.lower().strip()
        if new_key != old_key and new_key in self.contacts:
            return False, "Contact with new name already exists"
        
        # Update contact
        contact_data = {
            'name': name.strip(),
            'phone': phone.strip(),
            'email': email.strip(),
            'address': address.strip(),
            'created_at': self.contacts[old_key].get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
        
        # Remove old key if name changed
        if new_key != old_key:
            del self.contacts[old_key]
        
        self.contacts[new_key] = contact_data
        
        if self.save_contacts():
            return True, "Contact updated successfully"
        return False, "Failed to save contact"
    
    def delete_contact(self, name):
        name_key = name.lower().strip()
        if name_key not in self.contacts:
            return False, "Contact not found"
        
        del self.contacts[name_key]
        if self.save_contacts():
            return True, "Contact deleted successfully"
        return False, "Failed to delete contact"
    
    def get_stats(self):
        total = len(self.contacts)
        with_email = sum(1 for c in self.contacts.values() if c['email'])
        with_address = sum(1 for c in self.contacts.values() if c['address'])
        return {
            'total': total,
            'with_email': with_email,
            'with_address': with_address
        }

# Initialize contact manager
cm = ContactManager()

@app.route('/')
def index():
    search = request.args.get('search', '')
    contacts = cm.search_contacts(search)
    stats = cm.get_stats()
    return render_template('index.html', contacts=contacts, search=search, stats=stats)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        
        success, message = cm.add_contact(name, phone, email, address)
        if success:
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
    
    return render_template('add_contact.html')

@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_contact(name):
    contact = cm.get_contact(name)
    if not contact:
        flash('Contact not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_name = request.form['name']
        phone = request.form['phone']
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        
        success, message = cm.update_contact(name, new_name, phone, email, address)
        if success:
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
    
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete/<name>', methods=['POST'])
def delete_contact(name):
    success, message = cm.delete_contact(name)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))

@app.route('/api/contacts')
def api_contacts():
    search = request.args.get('search', '')
    contacts = cm.search_contacts(search)
    return jsonify(contacts)

@app.route('/api/stats')
def api_stats():
    return jsonify(cm.get_stats())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
