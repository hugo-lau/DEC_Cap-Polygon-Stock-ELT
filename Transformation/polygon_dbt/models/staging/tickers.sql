select
    name,
    type,
    locale,
    market,
    ticker,
    currency_name,
    last_updated_utc,
    primary_exchange
from {{ source('polygon','tickers')}}