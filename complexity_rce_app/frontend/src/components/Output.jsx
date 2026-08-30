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
            <div>
                <label>Code Output:</label>
                <pre style={{outputStyle}}> {output} </pre>
            </div>
            <p>Estimated complexity: {complexity}</p>
            <p>Certainty in estimate: {certainty} %</p>
            <p>Analysis strength: {analysisStrength}</p>
            <div>
                <h3>Dynamic Plotting: </h3>
                <DynamicPlotting complexity_model={estimated_function} params={parameters} points={dataPoints} />
            </div>
      </div>
    )
}

export default Output