import React from 'react';
import { Table } from 'react-bootstrap';

const StockData = ({ stockData }) => {
    const keys = Object.keys(stockData);
    const rows = Object.values(stockData[keys[0]]).map((_, index) => (
        <tr key={index}>
            {keys.map((key) => (
                <td key={key}>{stockData[key][index]}</td>
            ))}
        </tr>
    ));

    return (
        <div>
            <h2>Stock Data</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        {keys.map((key) => (
                            <th key={key}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </Table>
        </div>
    );
};

export default StockData;
