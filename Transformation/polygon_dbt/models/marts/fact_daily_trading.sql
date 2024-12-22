with daily_open_close as(
    select
        symbol as name,
        date as date,
        open as open,
        close as close,
        high as high,
        low as low,
        volume as volume,
        premarket as premarket,
        afterhours as afterhours
    from {{ ref('daily_open_close')}}
),
grouped_daily_ticker as(
    select
        T,
        date,
        N,
        VW
    from {{ref('grouped_daily')}}
)
select
    {{dbt_utils.generate_surrogate_key(['open_close.name'])}} as ticker_daily_key,
    open_close.name as symbol,
    open_close.date,
    open_close.open,
    open_close.close,
    open_close.low,
    open_close.high,
    open_close.volume,
    open_close.premarket,
    open_close.afterhours,
    grouped_daily_ticker.date as grouped_daily_date,
    grouped_daily_ticker.N as number_of_transactions,
    grouped_daily_ticker.VW as volume_weighted_avg
from daily_open_close as open_close
inner join grouped_daily_ticker as grouped_daily_ticker
    on grouped_daily_ticker.T = open_close.name
