import yfinance as yf

def download_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        return stock_data
    except Exception as e:
        return None
