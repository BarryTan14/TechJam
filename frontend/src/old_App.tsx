import React, { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 TechJam Frontend</h1>
        <p>Welcome to your new React application!</p>
        
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            Count is {count}
          </button>
          <p>
            Edit <code>src/App.tsx</code> and save to test HMR
          </p>
        </div>

        <div className="features">
          <h2>✨ Features</h2>
          <ul>
            <li>⚡ Vite for fast development</li>
            <li>⚛️ React 18 with TypeScript</li>
            <li>🎨 Modern CSS with Tailwind-like styling</li>
            <li>🔧 ESLint for code quality</li>
            <li>📦 Hot Module Replacement</li>
          </ul>
        </div>

        <div className="links">
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <a
            className="App-link"
            href="https://vitejs.dev"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn Vite
          </a>
        </div>
      </header>
    </div>
  )
}

export default App
