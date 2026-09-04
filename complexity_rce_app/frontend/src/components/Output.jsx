import DynamicPlotting from "./DynamicPlotting.jsx"
const outputStyle = {
  margin: 0,
  fontFamily: 'inherit',
  resize: 'both',
  overflow: 'auto',
  minWidth: '200px',
  minHeight: '100px',
};

const Output = ({output, complexity, certainty, analysisStrength, estimated_function, parameters, dataPoints}) => {
    return (
        <div>
            <h2>Output</h2>
            <ul className="parameters">
                <li>
                    <label>Code Output:</label>
                    <pre style={{outputStyle}}> {output} </pre>
                </li>
                <li>Estimated complexity: {complexity}</li>
                <li>Certainty in estimate: {certainty} %</li>
                <li>Analysis strength: {analysisStrength}</li>
            </ul>
            <div>
                <h3>Dynamic Plotting: </h3>
                <DynamicPlotting complexity_model={estimated_function} params={parameters} points={dataPoints} />
            </div>
      </div>
    )
}

export default Output