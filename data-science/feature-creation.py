# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, lag
from snowflake.snowpark.window import Window


def main(session: snowpark.Session): 
    # Your code goes here, inside the "main" handler.
    tableName = 'vw_ohlc'
    dataframe = session.table(tableName).order_by("timestamp")

    window_spec = Window.order_by("timestamp")
    
    dataframe = dataframe.with_column("diff", lag(col("open")).over(window_spec) - col("open"))
    # Print a sample of the dataframe to standard output.
    dataframe.show()

    # look into transformer feature creation

    # Return value will appear in the Results tab.
    return dataframe