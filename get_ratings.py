import yfinance as yf
import pandas as pd
from scipy import stats

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
    "Meta" : "META",
    "Google" : "GOOGL",
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

def get_forward_return(ticker, event_date, months):

    df = pricedata[ticker]
    df = df.copy()
    df.index = df.index.tz_localize(None)
    event_date = pd.to_datetime(event_date).tz_localize(None)
    target_date = event_date + pd.DateOffset(months = months)
    start_slice = df[df.index >= event_date]
    end_slice = df[df.index >= target_date]
    if start_slice.empty or end_slice.empty:
        return None
    start_price = start_slice.iloc[0]['Close']
    end_price = end_slice.iloc[0]['Close']

    return (end_price - start_price) / start_price

def run_tptest(df, rating_a, rating_b, horizon_col):

    a = df[df['rating'] == rating_a][horizon_col].dropna()
    b = df[df['rating'] == rating_b][horizon_col].dropna()
    t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)
    tps.append({
        'comparison': f"{rating_a} vs {rating_b}",
        'horizon': horizon_col,
        't_stat': t_stat,
        'p_value': p_value
    })

def get_spy_return(event_date, months):
    df = spy_df.copy()
    df.index = df.index.tz_localize(None)
    event_date = pd.to_datetime(event_date).tz_localize(None)
    target_date = event_date + pd.DateOffset(months = months)
    start_slice = df[df.index >= event_date]
    end_slice = df[df.index <= event_date]
    if start_slice.empty or end_slice.empty:
        return None
    start_price = start_slice.iloc[0]['Close']
    end_price = end_slice.iloc[0]['Close']
    return (end_price - start_price) / start_price

pricedata = {}
for i in stocks.values():
    pricedata[i] = yf.Ticker(i).history(period="13y")

all = []
for i in stocks.values():
    df = yf.Ticker(i).upgrades_downgrades
    df = df.reset_index()
    df = df[df['ToGrade'] != '']
    df['rating'] = df['ToGrade'].map(actions)
    df = df.dropna(subset=['rating'])
    df['ticker'] = i
    all.append(df)

spy_df = yf.Ticker("^GSPC").history(period="13y")

tps = []

master = pd.concat(all, ignore_index=True)
master['ret_1m'] = master.apply(lambda row: get_forward_return(row['ticker'], row['GradeDate'], 1), axis=1)
master['ret_3m'] = master.apply(lambda row: get_forward_return(row['ticker'], row['GradeDate'], 3), axis=1)
master['ret_6m'] = master.apply(lambda row: get_forward_return(row['ticker'], row['GradeDate'], 6), axis=1)
master['spy_ret_1m'] = master['GradeDate'].apply(lambda d: get_spy_return(d, 1))
master['spy_ret_3m'] = master['GradeDate'].apply(lambda d: get_spy_return(d, 3))
master['spy_ret_6m'] = master['GradeDate'].apply(lambda d: get_spy_return(d, 6))
master['excess_ret_1m'] = master['ret_1m'] - master['spy_ret_1m']
master['excess_ret_3m'] = master['ret_3m'] - master['spy_ret_3m']
master['excess_ret_6m'] = master['ret_6m'] - master['spy_ret_6m']

run_tptest(master, 'buy', 'sell', 'excess_ret_1m')
run_tptest(master, 'buy', 'sell', 'excess_ret_3m')
run_tptest(master, 'buy', 'sell', 'excess_ret_6m')
run_tptest(master, 'buy', 'hold', 'excess_ret_1m')
run_tptest(master, 'buy', 'hold', 'excess_ret_3m')
run_tptest(master, 'buy', 'hold', 'excess_ret_6m')
run_tptest(master, 'hold', 'sell', 'excess_ret_1m')
run_tptest(master, 'hold', 'sell', 'excess_ret_3m')
run_tptest(master, 'hold', 'sell', 'excess_ret_6m')
results_df = pd.DataFrame(tps)