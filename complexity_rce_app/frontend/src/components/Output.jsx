const Output = ({output, complexity, certainty, analysisStrength}) => {
    return (
        <div>
            <h2>Output</h2>
            <pre style={{ whiteSpace: 'pre-wrap', margin: 0, fontFamily: 'inherit' }}>
            Code Output: {output}
            </pre>
            <p>Estimated complexity: {complexity}</p>
            <p>Certainty in estimate: {certainty} %</p>
            <p>Analysis strength: {analysisStrength}</p>
      </div>
    )
}

export default Output