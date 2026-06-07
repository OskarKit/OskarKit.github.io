import yfinance as yf
import pandas as pd
import numpy as np
import json

def run_backtest(start_date="2022-01-01", end_date="2023-12-31"):
    print("Fetching historical market data...")

    # 1. Fetch Real Market Data
    # SPY = S&P 500 Benchmark, QQQ = Tech/Momentum proxy
    tickers = ['SPY', 'QQQ']
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    # 2. Calculate Daily Returns
    returns = data.pct_change().dropna()

    # 3. Define the "Algorithmic Strategy"
    # For this portfolio piece, we will simulate a Dual-Momentum Strategy.
    # When QQQ (Tech) outpaces SPY, we overweight QQQ. Otherwise, we hold SPY.
    # (Simplified here as a static 70/30 tech-heavy allocation for demonstration)
    algo_daily_returns = (returns['QQQ'] * 0.70) + (returns['SPY'] * 0.30)

    # Benchmark is just the S&P 500
    benchmark_daily_returns = returns['SPY']

    # 4. Calculate Cumulative Returns (Base 100)
    # This matches the "100" starting point on your HTML chart
    algo_cumulative = (1 + algo_daily_returns).cumprod() * 100
    benchmark_cumulative = (1 + benchmark_daily_returns).cumprod() * 100

    # 5. Resample Data to Quarterly for the Chart.js visualization
    algo_quarterly = algo_cumulative.resample('QE').last()
    benchmark_quarterly = benchmark_cumulative.resample('QE').last()

    # 6. Format Output for JavaScript / Web Frontend
    # Extract quarters for the X-axis labels (e.g., 'Q1', 'Q2')
    labels = [f"Q{date.quarter} {date.year}" for date in algo_quarterly.index]

    # Round data to 2 decimal places for clean UI presentation
    algo_data = algo_quarterly.round(2).tolist()
    benchmark_data = benchmark_quarterly.round(2).tolist()

    # Create the final JSON payload
    export_data = {
        "labels": labels,
        "algo_returns": algo_data,
        "benchmark_returns": benchmark_data
    }

    return export_data

if __name__ == "__main__":
    # Run the backtest and print the results
    results = run_backtest("2020-01-01","2026-03-01")

    print("\n=== BACKTEST COMPLETE ===")
    print("Copy and paste this data into your projects.html Chart.js config:\n")
    print(json.dumps(results, indent=4))
