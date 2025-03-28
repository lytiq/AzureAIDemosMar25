from typing import Any, Callable, Set, Dict, List, Optional
import json 
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span(name="stock_price_tool")
def get_stock_price(stock_symbol):
    """
    Get the current stock price for a given stock symbol using yfinance.
    
    :param: stock_symbol (str): The stock symbol/ticker (e.g., 'AAPL' for Apple)
        
    :return: A JSON string mapping containing key 'stock_price' and its value.
    :rtype: str
        
    Example:
        >>> price = get_stock_price('AAPL')
        >>> print(price)
        {"stock_price": 150.25}
    """
    try:
        import yfinance as yf
        
        # Get ticker data
        ticker = yf.Ticker(stock_symbol)
        
        # Get current price from info
        current_price = ticker.info['regularMarketPrice']

        result = json.dumps({"stock_price": current_price})
        
        trace.get_current_span().set_attributes({
            "input.stock_symbol": stock_symbol,
            "output.price": current_price
        })
        
        return result
        
    except Exception as e:


        error_msg = f"Error fetching stock price for {stock_symbol}: {str(e)}"
        trace.get_current_span().set_attributes({
            "input.stock_symbol": stock_symbol,
            "error": error_msg
        })
        return json.dumps({"stock_price": None})    
user_functions: Set[Callable[..., Any]] = {
    get_stock_price,
}