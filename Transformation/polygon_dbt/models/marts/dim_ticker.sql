select 
    {{dbt_utils.generate_surrogate_key(['t.ticker'])}} as ticker_key,
    t.name,
    t.ticker as ticker_name,
    t.type,
    t.currency_name,
    t.primary_exchange,
    tt.description,
    tt.asset_class as market_class
from {{ ref('tickers') }} as t
inner join {{ ref('ticker_types') }} as tt
    on t.type = tt.code
