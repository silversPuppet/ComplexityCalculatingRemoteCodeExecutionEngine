import { useState } from 'react'

const Input = ({onExecute}) => {
    const [code, setCode] = useState("#necessary for the server to execute user code properly \ndef main(n):\n return n\n")
    const [input, setInput] = useState("0")
    const [input_type, setInput_type] = useState("int")
    const [language, setLanguage] = useState("python")
    const [analyse_dynamically, setDynamic] = useState(true)
    const [analyse_statically, setStatic] = useState(true)

    const handleSubmit = (event) => {
      event.preventDefault()
      onExecute({ code, input, input_type, language, analyse_dynamically, analyse_statically })
    }

    return (
    <div>
        <h2>Input</h2>
        <form  onSubmit={handleSubmit}>
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
          <input value={input} onChange={e => setInput(e.target.value)}/>
          Dynamic Analysis:
          <input type='checkbox' checked={analyse_dynamically} onChange={e => setDynamic(e.target.checked)} />
          Static Analysis:
          <input type='checkbox' checked={analyse_statically}  onChange={e => setStatic(e.target.checked)} />
          <button type="submit">Submit</button>
          <br />
          <textarea 
            name="postContent" 
            rows={17} 
            cols={57} 
            value={code}
            onChange={e => setCode(e.target.value)}
          />
        </form>
      </div>
    )
}

export default Input 