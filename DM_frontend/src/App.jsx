import { useState } from 'react'
import './App.css'

function App() {
  const [username, setUsername] = useState('')
  const [journalEntry, setJournalEntry] = useState('')
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! How can I help you today?' },
    { role: 'user', content: 'Just testing the layout!' }
  ])

  const handleSaveEntry = () => {
    // This will be connected to the backend later
    console.log('Saving entry:', { username, journalEntry })
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