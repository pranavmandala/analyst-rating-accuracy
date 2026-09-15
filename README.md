# Do Analyst Ratings Predict Stock Returns?

## Question
Wall Street analysts issue buy/hold/sell ratings on stocks constantly, but do these ratings actually predict future performance — or are they closer to noise? This project tests whether stocks receiving "buy" ratings subsequently outperform stocks receiving "sell" ratings, relative to the broader market.

## Method
- Pulled analyst rating changes and price history for 30 large-cap stocks across tech, finance, and other sectors (e.g. AAPL, MSFT, NVDA, JPM, TSLA) using `yfinance`
- Covered roughly 13 years of data, ~18,000 individual rating events
- Normalized ~30 raw rating labels (e.g. "Overweight," "Sector Perform") into three categories: **buy**, **hold**, **sell**
- For each event, calculated the stock's forward return at 1, 3, and 6 months
- Subtracted the S&P 500's return over the same window to compute **excess return** — how much the stock outperformed or underperformed the broader market, independent of general market conditions
- Compared excess returns across rating categories using **t and p tests** to check whether observed differences were statistically meaningful or likely due to chance

**Tools:** Python, pandas, yfinance, scipy, Tableau

## Findings
Buy-rated stocks significantly outperformed sell-rated stocks in the month immediately following the rating change (**t = 4.14, p < 0.0001**), with a clear, wide gap in average excess returns. However, this edge weakened substantially by 3 months (**p = 0.072**) and had effectively disappeared — or slightly reversed — by 6 months (**p = 0.092**).

Buy-vs-hold comparisons showed the strongest and most consistent statistical significance across all horizons, likely reflecting hold's much larger sample size relative to sell.

**The takeaway:** analyst ratings appear to carry real short-term predictive signal, but that signal decays quickly rather than persisting. This is consistent with a market-efficiency explanation — any informational edge analysts have gets priced in fast, leaving little advantage for someone acting on the rating months later.

| Comparison | Horizon | t-value | p-value |
|---|---|---|---|
| buy vs sell | 1m | 4.0709 | 0.0001 |
| buy vs sell | 3m | 1.7973 | 0.0727 |
| buy vs sell | 6m | -1.584 | 0.0977 |
| buy vs hold | 1m | 8.0494 | <0.0001 |
| buy vs hold | 3m | 5.5738 | <0.0001 |
| buy vs hold | 6m | 2.2593 | <0.0239 |
| hold vs sell | 1m | 0.6342 | <0.5261 |
| hold vs sell | 3m | -0.6262 | <0.5314 |
| hold vs sell | 6m | -2.5277 | <0.0116 |
