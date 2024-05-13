create or replace table TF_TEST.DATA.land_ohlc (
    timestamp timestamp,
    open number,
    high float,
    low float,
    close float,
    volume float,
    trades number
);

create or replace table TF_TEST.DATA.ohlc (
    timestamp timestamp,
    trade_pair string,    
    open number,
    high float,
    low float,
    close float,
    volume float,
    trades number
);