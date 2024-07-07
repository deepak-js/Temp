import React from 'react';
import Plot from 'react-plotly.js';

const Heatmap = ({ drawdownPlot }) => {
    return (
        <div>
            <h2>Drawdown Heatmap</h2>
            <Plot data={drawdownPlot.data} layout={drawdownPlot.layout} />
        </div>
    );
};

export default Heatmap;
