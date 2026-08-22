import { useState, useEffect } from 'react'
import codeExecutionService from "./services/execution"
import Input from "./components/Input"
import Output from './components/Output'

function App() {
  const [session_id, setSession_id] = useState("no session ID")

  const [currentTask, setCurrentTask] = useState("")

  const [output, setOutput] = useState("")
  const [complexity, setComplexity] = useState("???")
  const [certainty, setCertainty] = useState(0)
  const [analysisStrength, setAnalysisStrength] = useState("")

  const uuid_hook = () => {
    console.log("effect hook")
    codeExecutionService.get_new_session_id()
      .then(uuid => {
        setSession_id(uuid)
      })
  }

  useEffect(uuid_hook, []) 

  const executeAnalyseCode = ({code, input, input_type, language}) => {
      codeExecutionService.start_execute_analysis_task(session_id, code, input, input_type, language)
        .then(result => {
          console.log(result)
          setCurrentTask(result.task_id)
          getCurrentTaskStatus(result.task_id)
        }).catch (error => console.log("Failed to execute and analyse user submitted code: ", error))
  }

  const getCurrentTaskStatus = (task_id) => {
    try{
      codeExecutionService.get_task_status(task_id, session_id)
        .then(response => {
          let result = response.result
          if(response.status === "completed"){
            console.log(result)
            setOutput(result.output)
            setComplexity(result.complexity)
            setCertainty(result.certainty)
            setAnalysisStrength(result.analysis_strength)
          }else if(response.status === "failed"){
            console.log("Error executing user script:\n" + result)
            setOutput(result)
            setComplexity("???")
            setCertainty(0)
            setAnalysisStrength("")
          }else{
            throw new Error("Task status could not be resolved.")
          }
        })
        
    }
    catch (error){
      console.log("Failed to acquire task status: ", error)
    }
  }

  return (
    <div>
      <h1>Complexity estimating RCE</h1>
      <p>Session: {session_id}</p>
      <p>Current Task: {currentTask}</p>
      <div className="content">
        <Input onExecute={executeAnalyseCode} />
        <Output output={output} complexity={complexity} certainty={certainty} analysisStrength={analysisStrength}  />
      </div>
    </div>
  )
}

export default App
