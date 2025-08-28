import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import Dashboard from './dashboard/App'
import Logs from './featureLogs/App'
import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path='/featureLogs' element={<Logs />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
