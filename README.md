# Plot Stock Data Description

## Overview
The PlotStocksPrices class provides functionality to download stock data, process it, and visualize the stock prices along with various statistical averages. It uses data from Yahoo Finance to analyze and plot stock prices, normalized volumes, and various moving averages. This class can handle multiple stock tickers, clean input data, and generate informative plots.

## Disclaimer

This project is for educational purposes only and does not constitute financial advice. Always do your own research or consult with a financial professional before making any investment decisions.

## Setup Instructions

### Prerequisites

- Ensure you have Git installed on your system.
- For Linux/Mac: Ensure you have `curl` installed.

### Clone the Repository

First, clone the Git repository to your local machine:

```sh
git clone https://github.com/gaber444/StockDataPlot.git
cd StockDataPlot
```

### For Linux/Mac
```sh
./setup_env.sh
```
### For Windows
```sh
windows_setup_env.bat
```

## Usage example
Here is an example of how to use the `PlotStocksPrices` class to download and plot stock data:

```python
# Define the date range and tickers
start_date: str = '2023-05-21'
end_date: str = '2024-05-21'
tickers: list = ['AAPL', 'MU']

# Initialize the PlotStocksPrices class with the list of tickers
m_stock = PlotStocksPrices(tickers)

# Set the start and end dates for the data to be downloaded
m_stock.SetStartEndDate(start_date, end_date)

# Download the data, process it, and generate plots
m_stock.combineAll()
