import React from 'react';

const Metrics = ({ metrics }) => {
    return (
        <div>
            <h2>Key Metrics</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {Object.entries(metrics).map(([key, value]) => (
                    <div key={key} style={{ flex: '25%', backgroundColor: '#2f4f4f', color: 'white', textAlign: 'center', fontSize: '18px', padding: '20px', margin: '10px', borderRadius: '10px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.4)' }}>
                        {key}: <br /><b>{value}</b>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Metrics;
