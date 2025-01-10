import { useState } from 'react'
import './App.css'

function App() {
  const [username, setUsername] = useState('')
  const [journalEntry, setJournalEntry] = useState('')
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! How can I help you today?' },
    { role: 'user', content: 'Just testing the layout!' }
  ])

  const handleSaveEntry = async () => {
    if (!username || !journalEntry) {
      alert('Please provide both username and journal entry');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/save-entry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          entry: journalEntry,
          timestamp: new Date().toISOString()
        })
      });

      if (response.ok) {
        alert('Journal entry saved successfully!');
        setJournalEntry(''); // Clear the entry after saving
      } else {
        alert('Failed to save journal entry');
      }
    } catch (error) {
      console.error('Error saving entry:', error);
      alert('Error saving journal entry');
    }
  }

  return (
    <div className="app-container">
      <div className="journal-section">
        <div className="username-container">
          <h2>Username</h2>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username..."
            className="username-input"
          />
        </div>
        <h2>Journal Entry</h2>
        <textarea
          value={journalEntry}
          onChange={(e) => setJournalEntry(e.target.value)}
          placeholder="Write your journal entry here..."
          className="journal-textarea"
        />
        <button 
          onClick={handleSaveEntry}
          className="save-button"
        >
          Save Entry
        </button>
      </div>

      <div className="chat-section">
        <h2>AI Conversation</h2>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              {message.content}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App