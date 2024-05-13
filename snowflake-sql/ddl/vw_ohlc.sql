create or replace view TF_TEST.DATA.vw_ohlc as
select
    trade_pair,
    timestamp,
    open,
    high,
    low,
    close,
    volume,
    trades
from TF_TEST.DATA.ohlc
order by timestamp
;