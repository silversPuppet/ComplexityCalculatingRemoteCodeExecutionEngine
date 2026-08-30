import React from 'react';
import Plot from 'react-plotly.js';

const DynamicPlotting  = ({complexity_model, params, points}) => {
    const functions = {
        constant: ([c], x) => c,
        logarithmic: ([a, b], x) => a * Math.log(x) + b,
        polynomial: ([a, k, b] , x) => a * (x ** k) + b,
        exponential: ([a, b, c], x) => a * Math.exp(b * x) + c
    }
    const model_function = (x) => functions[complexity_model](params, x)

    const xMin = Math.min(...points[0])
    const xMax = Math.max(...points[0])

    const padding = (xMax - xMin) * 0.1 || 1
    const curveStart = xMin - padding
    const curveEnd = xMax + padding

    const sampleCount = points[0].length * 10

    const curveX = Array.from({ length: sampleCount },   (_, i) =>curveStart + (curveEnd - curveStart) * (i / (sampleCount - 1)))

    const curveY = curveX.map(model_function)

    return (
      <Plot
      data={[

        {
          x: curveX,
          y: curveY,
          type: "scatter",
          mode: "lines",
          name: "Model",
        },
        {
          x: points[0],
          y: points[1],
          type: "scatter",
          mode: "markers",
          name: "Observed data",
          marker: {
            size: 8
          }
        }
      ]}
      layout={{
        autosize: true,
        title: {
          text: "Model vs observed data"
        },
        xaxis: {
          title: {
            text: "input n"
          }
        },
        yaxis: {
            autorange: true,
          title: {
            text: "time"
          }
        },
        hovermode: "closest"
      }}
      useResizeHandler
      style={{
        width: "70%",
        height: "400px"
      }}
    />
    );
}

export default DynamicPlotting
