select
    {{dbt_utils.generate_surrogate_key(['t.ticker'])}} as stock_split_key,
    t.ticker,
    s.split_to,
    s.split_from,
    s.execution_date,
from {{ ref('tickers')}} as t
inner join {{ ref('stock_split') }} as s
    on s.symbol = t.ticker
