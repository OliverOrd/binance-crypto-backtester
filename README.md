# Binance Crypto Trading Strategy Backtester

### Getting Started

Install the python dependencies using:
```pip install -r requirements.txt```


### Using the App

Use the command:```python .\get_price_data.py``` to download price data on timeframe/asset specified in ```get_price_data.py```.

Price data stored in ```data``` directory.

Run ```python .\ewma_optimize.py``` or ```python .\median_vol_optimize.py``` to find optimal lookback parameters for each strategy.

Run ```python .\convert_results.py``` to combine all results into a single .CSV file.

