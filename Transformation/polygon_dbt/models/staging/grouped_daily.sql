select
    T,
    N,
    date,
    VW
from {{ source('polygon','grouped_daily')}}