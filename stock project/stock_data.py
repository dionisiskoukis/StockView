# =====================================================================================================
# STOCK_DATA.PY - Yahoo Finance Data Fetching
# =====================================================================================================
# This file handles ALL communication with Yahoo Finance to get stock data
# It's a separate file to keep data fetching logic separate from the UI code
# This makes it easier to maintain and test the code
# =====================================================================================================

import yfinance as yf
from datetime import datetime

# =====================================================================================================
# STOCK DATA MANAGER CLASS
# =====================================================================================================
# This class is responsible for fetching and managing all stock data from Yahoo Finance
# It has methods for getting current prices, historical data, and company information
# All the complexity of dealing with Yahoo Finance API is hidden in this class

class StockDataManager:
    """
    Manager class that fetches and processes stock data from Yahoo Finance.
    This keeps all data-fetching logic in one place, making it easy to modify
    or switch to a different data source in the future.
    """

    # Constructor - runs when we create a new StockDataManager
    def __init__(self):
        """
        Initialize the StockDataManager.
        Currently just a placeholder, but could be used for caching in the future.
        """
        # Cache could be added here to store previously fetched data
        # This would make the app faster by avoiding repeated API calls
        pass

    # ================================================================================================
    # METHOD: Get Current Price and Direction
    # ================================================================================================
    def get_current_price(self, symbol):
        """
        Get the current price of a stock and determine if it went UP or DOWN.

        Parameters:
            symbol (str): The stock ticker symbol (e.g., "AAPL" for Apple)

        Returns:
            dict: A dictionary containing:
                - 'price': Current stock price (float)
                - 'direction': Either 'UP' (green), 'DOWN' (red), or 'NEUTRAL' (gray)
                - 'previous_price': The price from the previous minute
                - 'change': The price difference (current - previous)
                - 'error': Error message if something went wrong (or None if successful)

        How it works:
            1. Create a Ticker object for the stock symbol
            2. Get 1 minute interval data for today (this gives us minute-by-minute prices)
            3. Compare the latest price with the previous price
            4. Return green if price went up, red if down, gray if same
        """
        try:
            # Create a Ticker object - this is Yahoo Finance's way of accessing stock data
            ticker = yf.Ticker(symbol)

            # Get historical data for today, with 1-minute intervals
            # period="1d" means "get data for 1 day (today)"
            # interval="1m" means "get data for every 1 minute"
            data = ticker.history(period="1d", interval="1m")

            # Check if we actually got data (sometimes Yahoo Finance has issues)
            if data.empty or len(data) < 2:
                # Not enough data points to compare
                return {
                    'price': None,
                    'direction': 'NEUTRAL',
                    'previous_price': None,
                    'change': 0,
                    'error': f'Insufficient data for {symbol}'
                }

            # Get the current (latest) price - the last row of data
            current_price = data['Close'].iloc[-1]

            # Get the previous price - the second to last row of data
            previous_price = data['Close'].iloc[-2]

            # Calculate the change (difference between current and previous)
            change = current_price - previous_price

            # Determine the direction (UP, DOWN, or NEUTRAL)
            if current_price > previous_price:
                direction = 'UP'
            elif current_price < previous_price:
                direction = 'DOWN'
            else:
                direction = 'NEUTRAL'

            # Return all the information in a dictionary
            return {
                'price': float(current_price),
                'direction': direction,
                'previous_price': float(previous_price),
                'change': float(change),
                'error': None
            }

        except Exception as e:
            # If something goes wrong (network error, stock doesn't exist, etc.)
            # Return an error message instead of crashing
            return {
                'price': None,
                'direction': 'NEUTRAL',
                'previous_price': None,
                'change': 0,
                'error': f'Error fetching {symbol}: {str(e)}'
            }

    # ================================================================================================
    # METHOD: Get Intraday Chart Data
    # ================================================================================================
    def get_intraday_data(self, symbol):
        """
        Get minute-by-minute stock data for today (for charting).

        Parameters:
            symbol (str): The stock ticker symbol (e.g., "AAPL")

        Returns:
            pandas.DataFrame: A dataframe with timestamps and prices for each minute
                             or None if an error occurred

        How it works:
            1. Fetch 1-minute interval data for today
            2. Return the raw data for the chart to plot
        """
        try:
            # Create a Ticker object
            ticker = yf.Ticker(symbol)

            # Get 1-minute interval data for today
            # This returns a dataframe with columns: Open, High, Low, Close, Volume
            data = ticker.history(period="1d", interval="1m")

            # Check if we got any data
            if data.empty:
                return None

            # Return the dataframe (it has timestamps as index and Close prices as a column)
            return data

        except Exception as e:
            # If something goes wrong, return None
            print(f"Error fetching intraday data for {symbol}: {str(e)}")
            return None

    # ================================================================================================
    # METHOD: Get Stock Information (Market Cap, P/E Ratio, etc.)
    # ================================================================================================
    def get_stock_info(self, symbol):
        """
        Get detailed information about a stock (market cap, P/E ratio, etc.).

        Parameters:
            symbol (str): The stock ticker symbol (e.g., "AAPL")

        Returns:
            dict: A dictionary containing:
                - 'market_cap': Market capitalization (e.g., "2.8 Trillion")
                - 'pe_ratio': Price to Earnings ratio (e.g., "28.5")
                - 'dividend_yield': Dividend yield (e.g., "0.42%")
                - '52_week_high': Highest price in last 52 weeks
                - '52_week_low': Lowest price in last 52 weeks
                - 'day_high': Highest price today
                - 'day_low': Lowest price today
                - 'error': Error message if something went wrong (or None if successful)

        How it works:
            1. Create a Ticker object
            2. Access the .info attribute which has company information
            3. Extract specific fields and format them nicely
            4. Return all the information in a dictionary
        """
        try:
            # Create a Ticker object
            ticker = yf.Ticker(symbol)

            # Get the info dictionary - this contains lots of company information
            info = ticker.info

            # Helper function to format large numbers nicely
            # e.g., 2800000000000 becomes "2.8T" (2.8 Trillion)
            def format_number(value):
                if value is None:
                    return "N/A"
                if isinstance(value, str):
                    return value

                value = float(value)

                # If it's over a trillion
                if abs(value) >= 1_000_000_000_000:
                    return f"${value / 1_000_000_000_000:.2f}T"
                # If it's over a billion
                elif abs(value) >= 1_000_000_000:
                    return f"${value / 1_000_000_000:.2f}B"
                # If it's over a million
                elif abs(value) >= 1_000_000:
                    return f"${value / 1_000_000:.2f}M"
                # Otherwise just show it as is
                else:
                    return f"${value:.2f}"

            # Extract specific fields from the info dictionary
            # Use .get() so it returns "N/A" if the field doesn't exist

            market_cap = info.get('marketCap', 0)
            market_cap_str = format_number(market_cap) if market_cap else "N/A"

            pe_ratio = info.get('trailingPE', None)
            pe_ratio_str = f"{pe_ratio:.2f}" if pe_ratio else "N/A"

            dividend_yield = info.get('dividendYield', None)
            dividend_str = f"{dividend_yield * 100:.2f}%" if dividend_yield else "N/A"

            week_52_high = info.get('fiftyTwoWeekHigh', None)
            week_52_high_str = f"${week_52_high:.2f}" if week_52_high else "N/A"

            week_52_low = info.get('fiftyTwoWeekLow', None)
            week_52_low_str = f"${week_52_low:.2f}" if week_52_low else "N/A"

            day_high = info.get('dayHigh', None)
            day_high_str = f"${day_high:.2f}" if day_high else "N/A"

            day_low = info.get('dayLow', None)
            day_low_str = f"${day_low:.2f}" if day_low else "N/A"

            # Return all information in a dictionary
            return {
                'market_cap': market_cap_str,
                'pe_ratio': pe_ratio_str,
                'dividend_yield': dividend_str,
                '52_week_high': week_52_high_str,
                '52_week_low': week_52_low_str,
                'day_high': day_high_str,
                'day_low': day_low_str,
                'error': None
            }

        except Exception as e:
            # If something goes wrong, return error information
            print(f"Error fetching info for {symbol}: {str(e)}")
            return {
                'market_cap': "N/A",
                'pe_ratio': "N/A",
                'dividend_yield': "N/A",
                '52_week_high': "N/A",
                '52_week_low': "N/A",
                'day_high': "N/A",
                'day_low': "N/A",
                'error': f'Error fetching {symbol} info'
            }
