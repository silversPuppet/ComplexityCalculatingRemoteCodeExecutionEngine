import { useState } from 'react'

const Input = ({onExecute}) => {
    const [code, setCode] = useState("#necessary for the server to execute user code properly \ndef main(n):\n return n\n")
    const [input_value, setInput] = useState("0")
    const [input_type, setInput_type] = useState("int")
    const [language, setLanguage] = useState("python")
    const [analyse_dynamically, setDynamic] = useState(true)
    const [analyse_statically, setStatic] = useState(true)
    const [number_data_points, setDataPointNumber] = useState(5)

    const handleSubmit = (event) => {
      event.preventDefault()
      onExecute({ code, input_value, input_type, language,number_data_points, analyse_dynamically, analyse_statically})
    }

    return (
    <div>
        <h2>Input</h2>
        <form  onSubmit={handleSubmit}>
          <ul className="parameters">
            <li>
              <label>Language: </label> 
              <select defaultValue={language} onChange={e => setLanguage(e.target.value)}>
                <option value="python">Python</option>
              </select>
            </li>
            <li>
              <label>Input type: </label>
              <select defaultValue={input_type} onChange={e => setInput_type(e.target.value)}>
                <option value="int">Integer (e.g. 42)</option>
                <option value="string">String (e.g. egg)</option>
                <option value="float">Float (e.g. 1.0)</option>
                <option value="int[]">Integer Array (e.g. 1, 2, 3)</option>
              </select>
            </li>
            <li>
              <label>Input: </label>
              <input value={input_value} onChange={e => setInput(e.target.value)}/>
            </li>
            <li>
              <label>Dynamic Analysis: </label>
              <input type='checkbox' checked={analyse_dynamically} onChange={e => setDynamic(e.target.checked)} />
            </li>
            <li>
              <label>Number of test data points: {number_data_points} </label>
              <div>
                <input type="range" value={number_data_points} min="5" max="17" onChange={e => setDataPointNumber(e.target.value)} />
              </div>
            </li>
            <li>
              <label>Static Analysis: </label>
              <input type='checkbox' checked={analyse_statically}  onChange={e => setStatic(e.target.checked)} />
            </li>
          </ul>
          <textarea 
            name="postContent" 
            rows={19} 
            cols={52} 
            value={code}
            maxLength={1500}
            onChange={e => setCode(e.target.value)}
          />
          <br />
          <button type="submit">Submit</button>
        </form>
      </div>
    )
}

export default Input 