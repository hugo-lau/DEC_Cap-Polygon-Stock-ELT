select
    symbol,
    date,
    open,
    close,
    high,
    low,
    volume,
    premarket,
    afterhours
from {{ source('polygon','daily_open_close')}}
