# Binance Crypto Trading Strategy Backtester
![Alt text](screenshot.jpg?raw=true "Optional Title")

This software attempts to find optimal indicator parameters to maximise user returns for two trading strategies. Calculating momentum direction via median or exponential volatility.

Each parameter configuration/timeframe combination is run on its own process in parallel to speed things up.
### Getting Started

Install the python dependencies using:
```pip install -r requirements.txt```


### Using the App

Use the command: ```python .\get_price_data.py``` 

This downloads price data on timeframes/asset specified in ```get_price_data.py```

Price data is stored in ```data``` directory

Backtest results is stored in ```results``` directory

Run ```python .\ewma_optimize.py``` or ```python .\median_vol_optimize.py``` to find optimal lookback parameters for each strategy

Run ```python .\convert_results.py``` to combine all results into a single .CSV file

