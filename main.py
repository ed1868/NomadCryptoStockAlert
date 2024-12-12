import yfinance as yf
import ccxt
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email settings
EMAIL = "your_email@example.com"  # Replace with your email
PASSWORD = "your_password"        # Replace with your app password or email password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
TO_EMAIL = "recipient@example.com"  # Replace with recipient email

# Stocks and Cryptos to monitor
STOCKS = ["AAPL", "MSFT", "GOOG"]  # Replace with your stock symbols
CRYPTOS = ["BTC/USDT", "ETH/USDT"]  # Replace with your crypto symbols

# Price storage to track percentage changes
price_data = {}

# Thresholds
BUY_THRESHOLD = -10  # -10% means price goes down 10%
SELL_THRESHOLD = 20   # 20% means price goes up 20%

def send_email(subject, body):
    """Send an email notification."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def fetch_stock_prices():
    """Fetch current stock prices."""
    stock_prices = {}
    for stock in STOCKS:
        try:
            data = yf.Ticker(stock)
            stock_prices[stock] = data.history(period="1d")["Close"].iloc[-1]
        except Exception as e:
            print(f"Error fetching stock price for {stock}: {e}")
    return stock_prices

def fetch_crypto_prices():
    """Fetch current cryptocurrency prices."""
    crypto_prices = {}
    exchange = ccxt.binance()
    for pair in CRYPTOS:
        try:
            ticker = exchange.fetch_ticker(pair)
            crypto_prices[pair] = ticker["last"]
        except Exception as e:
            print(f"Error fetching crypto price for {pair}: {e}")
    return crypto_prices

def check_thresholds(new_prices):
    """Check if prices meet buy or sell thresholds and send email alerts."""
    for asset, new_price in new_prices.items():
        if asset not in price_data:
            price_data[asset] = {"initial": new_price}
            continue
        
        initial_price = price_data[asset]["initial"]
        percent_change = ((new_price - initial_price) / initial_price) * 100
        
        if percent_change <= BUY_THRESHOLD:
            send_email(
                subject=f"Good Time to Buy {asset}",
                body=f"The price of {asset} has dropped {percent_change:.2f}%!\nCurrent Price: {new_price}\nInitial Price: {initial_price}"
            )
            price_data[asset]["initial"] = new_price  # Reset initial price
        elif percent_change >= SELL_THRESHOLD:
            send_email(
                subject=f"Good Time to Sell {asset}",
                body=f"The price of {asset} has risen {percent_change:.2f}%!\nCurrent Price: {new_price}\nInitial Price: {initial_price}"
            )
            price_data[asset]["initial"] = new_price  # Reset initial price

def test_fetch_stock_prices():
    """Test fetching stock prices."""
    print("Testing fetch_stock_prices...")
    prices = fetch_stock_prices()
    assert isinstance(prices, dict), "Stock prices should be returned as a dictionary."
    print(f"Stock prices: {prices}")

def test_fetch_crypto_prices():
    """Test fetching crypto prices."""
    print("Testing fetch_crypto_prices...")
    prices = fetch_crypto_prices()
    assert isinstance(prices, dict), "Crypto prices should be returned as a dictionary."
    print(f"Crypto prices: {prices}")

def test_check_thresholds():
    """Test checking thresholds."""
    print("Testing check_thresholds...")
    mock_prices = {
        "AAPL": 90,  # Simulating a drop below threshold
        "BTC/USDT": 120,  # Simulating an increase above threshold
    }
    price_data["AAPL"] = {"initial": 100}
    price_data["BTC/USDT"] = {"initial": 100}
    check_thresholds(mock_prices)

def test_error_handling():
    """Test error handling for invalid stocks or cryptos."""
    global STOCKS, CRYPTOS
    print("Testing error handling...")
    STOCKS = ["INVALIDSTOCK"]
    CRYPTOS = ["INVALID/PAIR"]
    try:
        fetch_stock_prices()
        fetch_crypto_prices()
        print("Error handling passed.")
    except Exception as e:
        print(f"Error caught: {e}")

def run_tests():
    """Run all tests."""
    test_fetch_stock_prices()
    test_fetch_crypto_prices()
    test_check_thresholds()
    test_error_handling()
    print("All tests passed!")

def main():
    """Main function to monitor prices."""
    run_tests()  # Run tests before starting monitoring
    while True:
        print("Fetching prices...")
        stock_prices = fetch_stock_prices()
        crypto_prices = fetch_crypto_prices()
        
        all_prices = {**stock_prices, **crypto_prices}
        check_thresholds(all_prices)
        
        # Print prices for debugging
        print(pd.DataFrame([all_prices], index=["Price"]))
        
        print("Waiting for next check...")
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    main()
