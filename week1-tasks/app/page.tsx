"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, Edit, Trash2, Phone, Mail, MapPin, Users } from "lucide-react"

interface Contact {
  id: string
  name: string
  phone: string
  email?: string
  address?: string
  createdAt: string
}

export default function ContactManager() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingContact, setEditingContact] = useState<Contact | null>(null)

  // Load contacts from localStorage on component mount
  useEffect(() => {
    const savedContacts = localStorage.getItem("contacts")
    if (savedContacts) {
      setContacts(JSON.parse(savedContacts))
    }
  }, [])

  // Save contacts to localStorage whenever contacts change
  useEffect(() => {
    localStorage.setItem("contacts", JSON.stringify(contacts))
  }, [contacts])

  const filteredContacts = contacts.filter(
    (contact) =>
      contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      contact.phone.includes(searchTerm) ||
      contact.email?.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const addContact = (contactData: Omit<Contact, "id" | "createdAt">) => {
    const newContact: Contact = {
      ...contactData,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
    }
    setContacts([...contacts, newContact])
    setShowAddForm(false)
  }

  const updateContact = (id: string, contactData: Omit<Contact, "id" | "createdAt">) => {
    setContacts(contacts.map((contact) => (contact.id === id ? { ...contact, ...contactData } : contact)))
    setEditingContact(null)
  }

  const deleteContact = (id: string) => {
    if (confirm("Are you sure you want to delete this contact?")) {
      setContacts(contacts.filter((contact) => contact.id !== id))
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Users className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Contact Manager</h1>
            </div>
            <Badge variant="secondary" className="text-sm">
              {contacts.length} contacts
            </Badge>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Add Button */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search contacts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button onClick={() => setShowAddForm(true)} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Add Contact
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Contacts</p>
                  <p className="text-2xl font-bold text-gray-900">{contacts.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Mail className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">With Email</p>
                  <p className="text-2xl font-bold text-gray-900">{contacts.filter((c) => c.email).length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <MapPin className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">With Address</p>
                  <p className="text-2xl font-bold text-gray-900">{contacts.filter((c) => c.address).length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Contacts Grid */}
        {filteredContacts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContacts.map((contact) => (
              <ContactCard
                key={contact.id}
                contact={contact}
                onEdit={() => setEditingContact(contact)}
                onDelete={() => deleteContact(contact.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Users className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No contacts</h3>
            <p className="mt-1 text-sm text-gray-500">
              {searchTerm ? "No contacts match your search." : "Get started by creating a new contact."}
            </p>
            {!searchTerm && (
              <div className="mt-6">
                <Button onClick={() => setShowAddForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Add Contact
                </Button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Add/Edit Contact Modal */}
      {(showAddForm || editingContact) && (
        <ContactForm
          contact={editingContact}
          onSave={editingContact ? (data) => updateContact(editingContact.id, data) : addContact}
          onCancel={() => {
            setShowAddForm(false)
            setEditingContact(null)
          }}
        />
      )}
    </div>
  )
}

function ContactCard({
  contact,
  onEdit,
  onDelete,
}: {
  contact: Contact
  onEdit: () => void
  onDelete: () => void
}) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">{contact.name}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex items-center text-sm text-gray-600">
          <Phone className="h-4 w-4 mr-2" />
          {contact.phone}
        </div>
        {contact.email && (
          <div className="flex items-center text-sm text-gray-600">
            <Mail className="h-4 w-4 mr-2" />
            {contact.email}
          </div>
        )}
        {contact.address && (
          <div className="flex items-center text-sm text-gray-600">
            <MapPin className="h-4 w-4 mr-2" />
            {contact.address}
          </div>
        )}
        <div className="flex justify-end space-x-2 pt-4">
          <Button variant="outline" size="sm" onClick={onEdit}>
            <Edit className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={onDelete}>
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

function ContactForm({
  contact,
  onSave,
  onCancel,
}: {
  contact?: Contact | null
  onSave: (data: Omit<Contact, "id" | "createdAt">) => void
  onCancel: () => void
}) {
  const [formData, setFormData] = useState({
    name: contact?.name || "",
    phone: contact?.phone || "",
    email: contact?.email || "",
    address: contact?.address || "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.name && formData.phone) {
      onSave(formData)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>{contact ? "Edit Contact" : "Add New Contact"}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name *</label>
              <Input
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Phone *</label>
              <Input
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Address</label>
              <Input value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} />
            </div>
            <div className="flex justify-end space-x-2 pt-4">
              <Button type="button" variant="outline" onClick={onCancel}>
                Cancel
              </Button>
              <Button type="submit">{contact ? "Update" : "Add"} Contact</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
