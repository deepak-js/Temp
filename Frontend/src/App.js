import React, { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import axios from 'axios';
import Metrics from './components/Metrics';
import EquityCurve from './components/EquityCurve';
import Heatmap from './components/Heatmap';
import StockData from './components/StockData';

const App = () => {
    const [symbol, setSymbol] = useState('AAPL');
    const [startDate, setStartDate] = useState('2020-01-01');
    const [endDate, setEndDate] = useState('2022-01-01');
    const [stockData, setStockData] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [monthlyReturns, setMonthlyReturns] = useState(null);
    const [equityPlot, setEquityPlot] = useState(null);
    const [drawdownPlot, setDrawdownPlot] = useState(null);

    const fetchData = async () => {
        try {
            const response = await axios.get('/api/data', { params: { symbol, start_date: startDate, end_date: endDate } });
            setStockData(response.data);
        } catch (error) {
            console.error('Error fetching data', error);
        }
    };

    const backtestStrategy = async () => {
        try {
            const response = await axios.post('/api/backtest', { stock_data: stockData });
            setMetrics(response.data);

            const monthlyReturnsResponse = await axios.post('/api/monthly_returns', { stock_data: stockData });
            setMonthlyReturns(monthlyReturnsResponse.data);

            const equityPlotResponse = await axios.post('/api/equity_plot', { stock_data: stockData });
            setEquityPlot(equityPlotResponse.data);

            const drawdownPlotResponse = await axios.post('/api/drawdown_plot', { stock_data: stockData });
            setDrawdownPlot(drawdownPlotResponse.data);
        } catch (error) {
            console.error('Error backtesting strategy', error);
        }
    };

    return (
        <Container>
            <Row>
                <Col>
                    <h1>Intraday Trading Strategy Backtesting</h1>
                    <Form>
                        <Form.Group>
                            <Form.Label>Ticker Symbol</Form.Label>
                            <Form.Control type="text" value={symbol} onChange={(e) => setSymbol(e.target.value)} />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Start Date</Form.Label>
                            <Form.Control type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>End Date</Form.Label>
                            <Form.Control type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
                        </Form.Group>
                        <Button onClick={fetchData}>Fetch Data</Button>
                        <Button onClick={backtestStrategy}>Backtest Strategy</Button>
                    </Form>
                </Col>
            </Row>
            {metrics && <Metrics metrics={metrics} />}
            {equityPlot && <EquityCurve equityPlot={equityPlot} />}
            {drawdownPlot && <Heatmap drawdownPlot={drawdownPlot} />}
            {monthlyReturns && <StockData stockData={stockData} />}
        </Container>
    );
};

export default App;
