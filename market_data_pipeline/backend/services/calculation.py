import pandas as pd
from pandas import DateOffset

class PerformanceCalculator:
    def __init__(self, df, ticker, start_date, end_date, start_balance):
        # Filter by ticker
        df = df[df["ticker"] == ticker]
        # Filter by date range
        df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        
        if df.empty:
            raise ValueError(f"No data found for {ticker} in the given date range.")
        
        # Sort and store
        self.df = df.sort_values("date").reset_index(drop=True)
        self.start_balance = start_balance
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    # ----------------- Dividend Helpers ------------------------
    def final_amount_dividend_reinvested(self):
        # initial shares purchased at the first open price
        shares = self.start_balance / self.df["open"].iloc[0]

        for index, row in self.df.iterrows():
            if row["dividends"] > 0:
                #reinvest dividends at the close price of that day
                new_shares = (row["dividends"] * shares) / row["close"]
                shares += new_shares
        # final value = total shares * last close price
        return shares * self.df["close"].iloc[-1]

    def final_amount_no_reinvestment(self):
        shares = self.start_balance / self.df["open"].iloc[0]
        cash = 0
        for index, row in self.df.iterrows():
            if row["dividends"] > 0:
                cash += row["dividends"] * shares
        # final value = share value + accumulated cash
        return (shares * self.df["close"].iloc[-1]) + cash
    
    # ----------------- Internal Helper --------------------------
    def _percent_change(self, start_index, end_index):
        start = self.df["open"].iloc[start_index]
        end = self.df["close"].iloc[end_index]
        return (end - start) / start

    # --------------- Performance metrics -------------------------
    def best_day(self):
        index = self.df["close"].idxmax()
        return {
            "date": self.df.loc[index, "date"],
            "price": float(self.df.loc[index, "close"])
        }

    def three_month(self):
        cutoff = self.df["date"].iloc[-1] - pd.DateOffset(months=3)
        df_cut = self.df[self.df["date"] >= cutoff]
        if len(df_cut) < 2:
            return None
        return self._percent_change(df_cut.index[0], df_cut.index[-1])

    def one_year(self):
        cutoff = self.df["date"].iloc[-1] - pd.DataOffset(years=1)
        df_cut = self.df[self.df["date"] >= cutoff]
        if len(df_cut) < 2:
            return None
        return self._percent_change(df_cut.index[0], df_cut.index[-1])

    def five_years(self):
        return self._period_years(5)

    def ten_years(self):
        return self._period_years(10)

    # ----------------- Internal Helper --------------------------
    def _period_years(self, years):
        cutoff = self.df["date"].iloc[-1] - pd.DateOffset(years=years)
        df_cut = self.df[self.df["date"] >= cutoff]
        if len(df_cut) < 2:
            return None
        return self._percent_change(df_cut.index[0], df_cut.index[-1])

    # --------------- Performance metrics -------------------------
    def max_drawdown(self):
        prices = self.df["close"]
        # running max of the price series
        running_max = prices.cummax()
        # drawdown at each point
        drawdowns = (prices - running_max) / running_max
        #max drawdown is the most negative value
        return drawdowns.min()
    
    def gain_loss_ratio(self):
        # daily percentage return
        returns = self.df["close"].pct_change().dropna()
        gains = returns[returns > 0]
        losses = returns[returns < 0]

        if len(gains) == 0 or len(losses) == 0:
            return None # not enough data
        
        return gains.mean() / abs(losses.mean())
    
    def positive_period_percentage(self):
        returns = self.df["close"].pct_change().dropna()

        positive = (returns > 0).sum()
        total = len(returns)

        return (positive / total) * 100
    