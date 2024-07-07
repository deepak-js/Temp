import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from matplotlib.colors import ListedColormap

def backtest_strategy(stock_data):
    stock_data['Gap'] = stock_data['Open'] - stock_data['Close'].shift(1)
    stock_data['Gap_Percentage'] = ((stock_data['Open'] - stock_data['Close'].shift(1)) / stock_data['Close'].shift(1)) * 100
    stock_data['Long or Short'] = ''
    stock_data['Entry Price'] = 0.0
    stock_data['Exit Price'] = 0.0
    stock_data['Trade Result'] = 0.0

    for index, row in stock_data.iterrows():
        if row['Gap_Percentage'] > 2.0:
            stock_data.at[index, 'Long or Short'] = 'Short'
            stock_data.at[index, 'Entry Price'] = row['Open']
            stock_data.at[index, 'Exit Price'] = row['Close']
            stock_data.at[index, 'Trade Result'] = row['Open'] - row['Close']
        elif row['Gap_Percentage'] < -2.0:
            stock_data.at[index, 'Long or Short'] = 'Long'
            stock_data.at[index, 'Entry Price'] = row['Open']
            stock_data.at[index, 'Exit Price'] = row['Close']
            stock_data.at[index, 'Trade Result'] = row['Close'] - row['Open']
        else:
            stock_data.at[index, 'Long or Short'] = 'No Trade'

    total_trades = len(stock_data[stock_data['Long or Short'] != 'No Trade'])
    successful_trades = len(stock_data[(stock_data['Long or Short'] != '') & (stock_data['Trade Result'] > 0)])
    success_ratio = successful_trades / total_trades * 100
    total_returns = stock_data['Trade Result'].sum()
    stock_data['Profit/Loss %'] = (stock_data['Trade Result'] / stock_data['Close'].shift(1)) * 100
    overall_returns = stock_data['Profit/Loss %'].sum()

    num_long_trades = len(stock_data[stock_data['Long or Short'] == 'Long'])
    num_short_trades = len(stock_data[stock_data['Long or Short'] == 'Short'])
    failure_trades = total_trades - successful_trades
    volatility = stock_data['Profit/Loss %'].std()

    return {
        'total_trades': total_trades,
        'successful_trades': successful_trades,
        'success_ratio': success_ratio,
        'total_returns': total_returns,
        'num_long_trades': num_long_trades,
        'num_short_trades': num_short_trades,
        'failure_trades': failure_trades,
        'volatility': volatility,
        'overall_returns': overall_returns
    }

def calculate_monthly_returns(stock_data):
    monthly_returns = stock_data['Close'].resample('M').ffill().pct_change().dropna()
    monthly_returns = monthly_returns.groupby([monthly_returns.index.year, monthly_returns.index.month]).sum().unstack()
    return monthly_returns

def plot_drawdown(stock_data):
    V = stock_data['Close']
    stock_data['drawdown'] = (V - V.cummax()) / V.cummax()
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['drawdown'], label='Drawdown', color='red')
    plt.title('Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    return plt

def calculate_equity_drawdown(df):
    equity = (df['Profit/Loss %']).cumsum().to_frame()
    prev_high = 0
    for i, Return in equity.itertuples():
        prev_high = max(prev_high, Return)
        dd = (Return - prev_high)
        equity.loc[i, 'Drawdown %'] = dd if dd < 0 else 0
    return equity

def plot_equity_drawdown(equity):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Equity Analysis", "Drawdown"))
    fig.add_trace(go.Scatter(x=equity.index, y=equity['Profit/Loss %'], mode='lines', name='Equity', fill='tozeroy', line=dict(color='green', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=equity.index, y=equity['Drawdown %'], name='Drawdown', fill='tozeroy', line=dict(color='firebrick', width=1.5)), row=2, col=1)
    fig.update_layout(title='Equity Analysis and Drawdown', xaxis_title='Date', yaxis_title='%', template='plotly_dark')
    return fig
