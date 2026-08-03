import {BrowserRouter, Routes, Route } from "react-router-dom"
import { useState, useEffect } from 'react'

import Header from './components/common/Header'
import Footer from './components/common/Footer'
import Loading from './components/common/Loading'
import Main from './pages/Main'
import Join from './pages/Join'
import Login from './pages/Login'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
        
        <Header />
        <Routes>
            <Route path="/" element={<Main />}/>
            <Route path="/login" element={<Login />} />
            <Route path="/join" element={<Join />} />
        </Routes>
        <Footer />
      
    </>
  )
}

export default App
