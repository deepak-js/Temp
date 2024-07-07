import React from 'react';
import Plot from 'react-plotly.js';

const EquityCurve = ({ equityPlot }) => {
    return (
        <div>
            <h2>Equity Curve</h2>
            <Plot data={equityPlot.data} layout={equityPlot.layout} />
        </div>
    );
};

export default EquityCurve;
