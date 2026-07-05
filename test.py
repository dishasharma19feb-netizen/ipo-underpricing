import yfinance as yf
data = yf.download("AFCB", start="2010-01-01", end="2010-02-01", progress=False, auto_adjust=True)
print(data)