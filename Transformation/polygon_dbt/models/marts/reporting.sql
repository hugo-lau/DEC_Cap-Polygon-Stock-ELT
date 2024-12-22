-- Create a CTE for deduplication
with deduplicated_trading as (
    select 
        *,
        row_number() over (
            partition by symbol, date 
            order by number_of_transactions desc
        ) as rn
    from {{ ref('fact_daily_trading')}} 
)

select
    -- Explicitly list columns instead of using star
    fdt.symbol,
    fdt.date,
    fdt.open,
    fdt.close,
    fdt.low,
    fdt.high,
    fdt.volume,
    fdt.premarket,
    fdt.afterhours,
    fdt.number_of_transactions,
    fdt.volume_weighted_avg,
    
    -- Ticker dimensions
    dt.name as company_name,
    dt.type as security_type,
    dt.currency_name,
    dt.description,
    dt.market_class,
    
    -- Exchange dimensions
    de.exchange_name,
    de.exchange_type,
    de.locale,
  
from deduplicated_trading as fdt
    left join {{ ref('dim_ticker') }} as dt
        on fdt.symbol = dt.ticker_name
    left join {{ ref('dim_exchange')}} as de
        on dt.primary_exchange = de.mic
where fdt.rn = 1  -- Take only the first row for each symbol/date combination