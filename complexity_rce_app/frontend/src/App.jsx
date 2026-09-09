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

  const [estimated_function, setFunction] = useState("constant")
  const [parameters, setParams] = useState([0.0])
  const [dataPoints, setDataPoints] = useState([[1, 2, 3, 4, 5] , [0, 0, 0, 0, 0]])

  const [loading, setLoading] = useState(false)

  const uuid_hook = () => {
    console.log("effect hook")
    codeExecutionService.get_new_session_id()
      .then(uuid => {
        setSession_id(uuid)
      })
  }

  useEffect(uuid_hook, []) 

  const executeAnalyseCode = ({code, input_value, input_type, language,number_data_points, analyse_dynamically, analyse_statically}) => {
      codeExecutionService.start_execute_analysis_task(session_id, code, input_value, input_type, language, number_data_points, analyse_dynamically, analyse_statically)
        .then(result => {
          console.log(result)
          setCurrentTask(result.task_id)
          getCurrentTaskStatus(result.task_id)
        }).catch (error => console.log("Failed to execute and analyse user submitted code: ", error))
  }

  const getCurrentTaskStatus = (task_id) => {
    try{
      setLoading(true)
      codeExecutionService.get_task_status(task_id, session_id)
        .then(response => {
          let result = response.result
          if(response.status === "completed"){
            console.log(result)
            setOutput(result.output)
            setComplexity(result.complexity)
            setCertainty(result.certainty)
            setAnalysisStrength(result.analysis_strength)
            setFunction(result.model_function)
            setParams(result.parameters)
            setDataPoints(result.dynamic_data_points)
          }else if(response.status === "failed"){
            console.log("Error executing user script:\n" + result)
            setOutput(result)
            setComplexity("???")
            setCertainty(0)
            setAnalysisStrength("")
          }else{
            throw new Error("Task status could not be resolved.")
          }
          setLoading(false)
        })
        
    }
    catch (error){
      console.log("Failed to acquire task status: ", error)
    }
  }

  const Loader = ({active}) => {
    if(active){
      return(
      <div className="loader"></div>
    )
    }
    else{
      return (
        <p>No submitted tasks.</p>
      )
    }
  }

  return (
    <div>
      <h1>Complexity estimating RCE</h1>
      <p>This website attempts to estimate a codes time complexity via empirical measurements and static syntax-tree analysis.</p>
      <p>A session and task id are given out to keep track of analysis requests. User code is not being stored.</p>
      <p>Current Task uuid: {currentTask}</p>
      <Loader active={loading} />
      <hr></hr>
      <div className="content">
        <Input onExecute={executeAnalyseCode} />
        <Output output={output} complexity={complexity} certainty={certainty} analysisStrength={analysisStrength} estimated_function={estimated_function} parameters={parameters} dataPoints={dataPoints} />
      </div>
      <footer>
        <div className="footer">
            <ul>
              <h4>Silver's Puppet</h4>
              <li><a href="https://github.com/silversPuppet" className="link">GitHub</a></li>
              <li><a href="https://github.com/silversPuppet/ComplexityCalculatingRemoteCodeExecutionEngine" className="link">Source code</a></li>
            </ul>
        </div>
      </ footer>
    </div>
  )
}

export default App
