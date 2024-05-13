--copy data into landing table
copy into TF_TEST.DATA.land_ohlc
from @TF_TEST.DATA.KRAKEN_DEV_STAGE/XBTUSD_1.csv
file_format = (type = csv)
;

--insert into main table and add trade pair
--adding an order by clause to ensure the data is inserted in the correct order for micropartitioning
insert into TF_TEST.DATA.ohlc
select
    timestamp,
    'XBTUSD' as trade_pair,
    open,
    high,
    low,
    close,
    volume,
    trades
from TF_TEST.DATA.land_ohlc
order by timestamp, trade_pair
;