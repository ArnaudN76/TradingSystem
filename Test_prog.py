import ta
import pandas as pd
import numpy as np


def Tasuki_bullish(df, open_c="open", close_c="close",high_c="high",low_c="low"):

    """
    Mastering Financial Pattern Recognition
    Sofien Kaabar
    Chapter 4. Classic Trend-Following Patterns
    If the close price from two periods ago is greater than the open price from two periods ago,
    the open price from one period ago is greater than the close two periods ago,
    the close price from one period ago is greater than the open price from one period ago,
    and the current close price is greater than the close price two periods ago, print 1 for buy signals.
    """
    df.copy()

    open = df[open_c]
    close = df[close_c]
    high = df[high_c]
    low = df[low_c]


    df['Tasuki_bullish']=0
    df.loc[(close.shift(2)>open.shift(2)) \
        & (open.shift(1)>close.shift(2)) \
        & (close.shift(1)>open.shift(1)) \
        & (close>close.shift(2)),'Tasuki_bullish']=1

    return df

#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////

def Tasuki_bearsih(df, open_c="open", close_c="close", high_c="high", low_c="low"):
    """

    Mastering Financial Pattern Recognition
    Sofien Kaabar
    Chapter 4. Classic Trend-Following Patterns

    If the close price from two periods ago is lower than the open price from two periods ago,
    the open price from one period ago is lower than the close two periods ago,
    the close price from one period ago is lower than the open price from one period ago,
    and the current close price is lower than the close price two periods ago,
    then print −1 for sell signals.
    """
    df.copy()

    open = df[open_c]
    close = df[close_c]
    high = df[high_c]
    low = df[low_c]


    df['Tasuki_bearsih']=0
    df.loc[(close.shift(2) < open.shift(2)) \
            & (open.shift(1) < close.shift(2)) \
            & (close.shift(1) < open.shift(1)) \
            & (close < close.shift(2)),'Tasuki_bearsih']=-1

    return df


def atr(df, n):
    df = df.copy()
    df[f"ATR"] = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"], int(n)).average_true_range()
    return df

#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////





class IndicateursDF:

    def __init__(self, data):

        self.data=data
        self.get_features()




    def get_features(self):
        self.data = Tasuki_bullish(self.data, "open", "close", "high", "low")
        self.data = Tasuki_bearsih(self.data, "open", "close", "high", "low")
        self.data=atr(self.data,14)

# Condition pour exécuter le code si le fichier est exécuté en tant que script
if __name__ == "__main__":

    # import data dans  DF
    df = pd.read_csv("../Data/FixTimeBars/AUDUSD_4H_Admiral_READY.csv", index_col="time", parse_dates=True)

    df=atr(df,14)
    # initialisation de la classe
    stg=IndicateursDF(data=df)

    # ajout des indicateurs dans le dataframe
    stg.get_features()
   

    list_col=['Tasuki_bullish','Tasuki_bearsih','ATR']
    # pour savoir le nombre de signal
    for name in list_col:
        print(name + " " + str(df[name].sum()) )