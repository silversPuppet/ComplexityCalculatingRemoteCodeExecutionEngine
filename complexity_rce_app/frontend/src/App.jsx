import { useState, useEffect } from 'react'
import codeExecutionService from "./services/execution"

function App() {
  const [session_ID, setSession_ID] = useState("no session ID")

  const [code, setCode] = useState("")
  const [input, setInput] = useState("")
  const [input_type, setInput_type] = useState("int")
  const [language, setLanguage] = useState("python")

  const [output, setOutput] = useState("")
  const [complexity, setComplexity] = useState("???")
  const [certainty, setCertainty] = useState(0)
  const [analysisStrength, setAnalysisStrength] = useState("")

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
    codeExecutionService.start_execute_analysis_task(session_ID, code, input, input_type, language)
      .then(result => {
        setOutput(result.output)
      })
  }

  return (
    <div>
      <h1>Complexity estimating RCE</h1>
      <div>
        <h2>Input</h2>
        <label>We have: {session_ID}</label>
        <form  onSubmit={executeAnalyseCode}>
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
          <button type="submit">Submit</button>
          <br />
          <textarea 
            name="postContent" 
            rows={17} 
            cols={57} 
            defaultValue={code}
          />
        </form>
      </div>
      <div>
        <h2>Output</h2>
        <p>Code Output: {output}</p>
        <p>Estimated complexity: {complexity}</p>
        <p>Certainty in estimate: {certainty} %</p>
        <p>Analysis strength: {analysisStrength}</p>
      </div>
    </div>
  )
}

export default App
