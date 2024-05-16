# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

# Calculate technical indicators
def calculate_technical_indicators(df):
    # Simple Moving Average (SMA)
    df['SMA_5'] = df['CLOSE'].rolling(window=5).mean()
    df['SMA_10'] = df['CLOSE'].rolling(window=10).mean()
    
    # Exponential Moving Average (EMA)
    df['EMA_5'] = df['CLOSE'].ewm(span=5, adjust=False).mean()
    df['EMA_10'] = df['CLOSE'].ewm(span=10, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    delta = df['CLOSE'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Moving Average Convergence Divergence (MACD)
    ema_12 = df['CLOSE'].ewm(span=12, adjust=False).mean()
    ema_26 = df['CLOSE'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['Middle_Band'] = df['CLOSE'].rolling(window=20).mean()
    df['Upper_Band'] = df['Middle_Band'] + (df['CLOSE'].rolling(window=20).std() * 2)
    df['Lower_Band'] = df['Middle_Band'] - (df['CLOSE'].rolling(window=20).std() * 2)
    
    return df

def main(session: snowpark.Session): 
    tableName = 'vw_ohlc'
    snowframe = session.table(tableName).order_by("timestamp")

    # Print a sample of the dataframe to standard output.
    df = snowframe.to_pandas()
    df = calculate_technical_indicators(df)

    print(df.head())
    snowframe = session.create_dataframe(df)
    
    # Return value will appear in the Results tab.
    return snowframe
