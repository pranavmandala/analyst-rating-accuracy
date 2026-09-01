import yfinance as yf
import pandas as pd

stocks = {
    "Nvidia" : "NVDA",
    "Apple" : "AAPL",
    "Microsoft" : "MSFT",
    "AMD" : "AMD",
    "Intel" : "INTC",
    "Cisco" : "CSCO",
    "Oracle" : "ORCL",
    "IBM" : "IBM",
    "Adobe" : "ADBE",
    "Salesforce" : "CRM",
    "Uber" : "UBER",
    "JP Morgan" : "JPM",
    "Visa" : "V",
    "Mastercard" : "MA",
    "Wells Fargo" : "WFC",
    "Morgan Stanley" : "MS",
    "American Express" : "AXP",
    "Bank of America" : "BAC",
    "Amazon" : "AMZN",
    "Tesla" : "TSLA",
    "Meta" : "Meta",
    "Google" : "Googl",
    "Netflix" : "NFLX",
    "Disney" : "DIS",
    "Verizon" : "VZ",
    "Costco" : "COST",
    "Sandisk" : "SNDK",
    "HP" : "HPE",
    "Motorola" : "MSI",
    "Airbnb" : "ABNB",
    "DoorDash" : "DASH"
}

actions = {
    "Overweight": "buy",
    "Outperform": "buy",
    "Buy": "buy",
    "Strong Buy": "buy",
    "Positive": "buy",
    "Market Outperform": "buy",
    "Sector Outperform": "buy",
    "Accumulate": "buy",
    "Outperformer": "buy",
    "Top Pick": "buy",
    "Long-Term Buy": "buy",
    "Neutral": "hold",
    "Hold": "hold",
    "Market Perform": "hold",
    "Equal-Weight": "hold",
    "Equal-weight": "hold",
    "Perform": "hold",
    "Peer Perform": "hold",
    "Sector Weight": "hold",
    "Sector Perform": "hold",
    "Fair Value": "hold",
    "Average": "hold",
    "In-Line": "hold",
    "Market Weight": "hold",
    "Mixed": "hold",
    "Underperform": "sell",
    "Underweight": "sell",
    "Reduce": "sell",
    "Sell": "sell",
    "Market Underperform": "sell",
    "Negative": "sell",
}

pricedata = {}
for i in stocks.values():
    pricedata[i] = yf.Ticker(i).history(period="max")

all = []
for i in stocks.values():
    df = yf.Ticker(i).upgrades_downgrades
    df = df.reset_index()
    df = df[df['ToGrade'] != '']
    df['rating'] = df['ToGrade'].map(actions)
    df = df.dropna(subset=['rating'])
    df['ticker'] = i
    all.append(df)

master = pd.concat(all, ignore_index=True)