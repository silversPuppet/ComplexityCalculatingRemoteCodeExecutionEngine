import { useState, useEffect } from 'react'
import codeExecutionService from "./services/execution"

function App() {
   const [session_ID, setSession_ID] = useState("no session ID")

   const [code, setCode] = useState("")
   const [input, setInput] = useState("")
   const [input_type, setInput_type] = useState("int")
   const [language, setLanguage] = useState("python")

  const uuid_hook = () => {
    console.log("effect hook")
    codeExecutionService.get_new_session_id()
      .then(uuid => {
        setSession_ID(uuid)
      })
  }

  useEffect(uuid_hook, []) 

  const executeAnalyseCode = event => {
    event.preventDefault()
    const codeTaskRequest = {
      session_id: session_ID,
      code: code,
      input: input,
      input_type: input_type,
      language: language
    }
  }

  return (
    <div>
      <h1>Complexity estimating RCE</h1>
      <div onSubmit={executeAnalyseCode}>
        <label>We have: {session_ID}</label>
        <form>
          Language: 
          <select defaultValue={language} onChange={e => setLanguage(e.target.value)}>
            <option value="python">Python</option>
            <option value="c++">c++ (to be added)</option>
          </select>
          Input type: 
          <select defaultValue={input_type} onChange={e => setInput_type(e.target.value)}>
            <option value="int">Integer</option>
            <option value="str">String</option>
          </select>
          Input:
          <input placeholder="..." onChange={e => setInput(e.target.value)}/>
          <br />
          <textarea 
            name="postContent" 
            rows={17} 
            cols={57} 
            defaultValue={code}
          />
        </form>
      </div>
    </div>
  )
}

export default App
