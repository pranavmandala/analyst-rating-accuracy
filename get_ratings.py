import yfinance as yf
import pandas as pd

ticker = yf.Ticker("META")
events = ticker.upgrades_downgrades
df = pd.DataFrame(events)

actions = {
    "Overweight" : "buy",
    "Outperform" : "buy",
    "Buy" : "buy",
    "Strong Buy" : "buy",
    "Positive" : "buy",
    "Market Outperform" : "buy",
    "Sector Outperform" : "buy",
    "Neutral" : "hold",
    "Hold": "hold",
    "Market Perform" : "hold",
    "Equal-Weight" : "hold",
    "Perform" : "hold",
    "Peer Perform" : "hold",
    "Sector Weight" : "hold",
    "Sector Perform" : "hold",
    "Underperform" : "sell",
    "Underweight" : "sell",
    "Reduce" : "sell",
    "Sell" : "sell"
}

for i in df['ToGrade']:
    if i in actions:
        continue
    else:
        print(i)