import requests
from config import url, headers, logger

def connect_to_api(): # Function to connect to the API and fetch stock data
    stocks = ['TSLA', 'MSFT', 'GOOGL'] # List of stock symbols to fetch data for
    json_response = []

    for stock in range(len(stocks)):
        querystring = {
             "function": "TIME_SERIES_INTRADAY",
             "symbol": f"{stocks[stock]}",
             "outputsize": "compact",
             "interval": "5min",
             "datatype": "json"
             }
        
        try:
            response = requests.get(url, headers = headers, params = querystring) # Make the API request to fetch stock data for the given symbol
            response.raise_for_status()  # Check for HTTP errors 
            data = response.json()
            logger.info(f"Stocks successfully loaded for {stocks[stock]}") # Log successful loading of stock data
            json_response.append(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error on stock: {e}")
            break
    return json_response

def extract_json(response): # Function to extract relevant data from the JSON response
    records = []
    for data in response:
        symbol = data["Meta Data"]["2. Symbol"]
        for date_str, metrics in data['Time Series (5min)'].items():
            record = {
                "symbol": symbol,
                "date": date_str,
                "open": metrics["1. open"],
                "high": metrics["2. high"],
                "low": metrics["3. low"], 
                "close": metrics["4. close"]      
            }
            records.append(record)
    return records