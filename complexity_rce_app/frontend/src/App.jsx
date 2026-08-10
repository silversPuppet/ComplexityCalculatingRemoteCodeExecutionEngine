import { useState, useEffect } from 'react'
import codeExecutionService from "./services/execution"

function App() {
   const [session_ID, setSession_ID] = useState("no session ID")

  const uuid_hook = () => {
    console.log("effect hook")
    codeExecutionService.get_new_session_id()
      .then(uuid => {
        setSession_ID(uuid)
      })
  }

  useEffect(uuid_hook, []) 

  return (
    <div>
      <h1>Complexity estimating RCE</h1>
      <div>
        <label>We have: {session_ID}</label>
      </div>
    </div>
  )
}

export default App
