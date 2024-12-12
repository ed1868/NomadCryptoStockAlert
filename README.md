# Stock and Crypto Price Monitor

## Overview
This script monitors specified stock symbols and cryptocurrency pairs for price changes. When a price meets certain thresholds:
- **Down 10%**: A "Good Time to Buy" email alert is sent.
- **Up 20%**: A "Good Time to Sell" email alert is sent.

The script runs continuously, checking prices at regular intervals.

---

## Features
- **Stock Monitoring**: Fetches stock prices using the `yfinance` library.
- **Crypto Monitoring**: Fetches cryptocurrency prices using the Binance API via `ccxt`.
- **Email Alerts**: Sends email notifications for buy or sell signals.
- **Threshold Detection**: Customizable thresholds for detecting significant price changes.
- **Error Handling**: Handles invalid stock symbols, API errors, and connection issues.
- **Testing Suite**: Includes test functions to validate core features.

---

## Requirements
Ensure you have the following libraries installed:

```bash
pip install yfinance ccxt pandas
```

---

## Configuration
Update the following settings in the script:

1. **Email Settings**:
   - Replace placeholders with your email credentials:
     ```python
     EMAIL = "your_email@example.com"  # Your email
     PASSWORD = "your_password"        # Your email password or app-specific password
     TO_EMAIL = "recipient@example.com"  # Recipient email
     ```
   - Gmail users: Enable *Allow Less Secure Apps* or generate an *App Password*.

2. **Stock and Crypto Symbols**:
   - Update `STOCKS` with the stock symbols you want to monitor:
     ```python
     STOCKS = ["AAPL", "MSFT", "GOOG"]  # Replace with your stock symbols
     ```
   - Update `CRYPTOS` with Binance trading pairs:
     ```python
     CRYPTOS = ["BTC/USDT", "ETH/USDT"]  # Replace with your crypto symbols
     ```

3. **Thresholds**:
   - Adjust `BUY_THRESHOLD` and `SELL_THRESHOLD` to define price change percentages:
     ```python
     BUY_THRESHOLD = -10  # -10% drop triggers a buy alert
     SELL_THRESHOLD = 20  # 20% rise triggers a sell alert
     ```

---

## Running the Script
Run the script using Python:

```bash
python stock_crypto_monitor.py
```

### Behavior:
1. The script performs initial price checks for all stocks and cryptocurrencies.
2. It continuously monitors prices every hour (adjustable via `time.sleep`).
3. Emails are sent when thresholds are met.

---

## Testing
The script includes the following test functions:
- **`test_fetch_stock_prices()`**: Verifies stock price fetching.
- **`test_fetch_crypto_prices()`**: Verifies crypto price fetching.
- **`test_check_thresholds()`**: Tests threshold detection for buy/sell signals.
- **`test_error_handling()`**: Tests error handling for invalid symbols.

To run all tests, the script executes `run_tests()` before monitoring begins.

---

## Error Handling
- Handles invalid stock symbols and cryptocurrency pairs gracefully.
- Prints informative messages for API failures or network issues.

---

## Example Email Alerts
**Buy Alert**:
```
Subject: Good Time to Buy AAPL
Body:
The price of AAPL has dropped -10.5%!
Current Price: $90.00
Initial Price: $100.00
```

**Sell Alert**:
```
Subject: Good Time to Sell BTC/USDT
Body:
The price of BTC/USDT has risen 20.0%!
Current Price: $120.00
Initial Price: $100.00
```

---

## Notes
- Ensure a stable internet connection.
- The Binance API requires public access for fetching crypto prices.
- Adjust the monitoring interval (`time.sleep`) as needed.

---

## Future Improvements
- Add support for additional exchanges and stock APIs.
- Implement SMS notifications.
- Enable persistent data storage for price tracking across script restarts.

---

## License
This project is licensed under the MIT License.

---

## Author
Eddie Ruiz
