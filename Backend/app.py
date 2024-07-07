from flask import Flask, request, jsonify, render_template
from data_fetch import download_data
from calculations import (
    backtest_strategy,
    calculate_monthly_returns,
    plot_drawdown,
    plot_equity_drawdown,
    calculate_equity_drawdown
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    stock_data = download_data(symbol, start_date, end_date)
    if stock_data is None:
        return jsonify({'error': 'Failed to fetch data'}), 500
    return stock_data.to_json()

@app.route('/api/backtest', methods=['POST'])
def backtest():
    data = request.json
    stock_data = pd.read_json(data['stock_data'])
    results = backtest_strategy(stock_data)
    return jsonify(results)

@app.route('/api/monthly_returns', methods=['POST'])
def monthly_returns():
    data = request.json
    stock_data = pd.read_json(data['stock_data'])
    monthly_returns = calculate_monthly_returns(stock_data)
    return monthly_returns.to_json()

@app.route('/api/equity_drawdown', methods=['POST'])
def equity_drawdown():
    data = request.json
    stock_data = pd.read_json(data['stock_data'])
    equity_drawdown = calculate_equity_drawdown(stock_data)
    return equity_drawdown.to_json()

@app.route('/api/drawdown_plot', methods=['POST'])
def drawdown_plot():
    data = request.json
    stock_data = pd.read_json(data['stock_data'])
    plot = plot_drawdown(stock_data)
    return plot

@app.route('/api/equity_plot', methods=['POST'])
def equity_plot():
    data = request.json
    stock_data = pd.read_json(data['stock_data'])
    equity_drawdown = calculate_equity_drawdown(stock_data)
    plot = plot_equity_drawdown(equity_drawdown)
    return plot

if __name__ == '__main__':
    app.run(debug=True)
