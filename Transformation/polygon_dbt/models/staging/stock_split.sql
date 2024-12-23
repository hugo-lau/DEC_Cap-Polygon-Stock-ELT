select  
    Ticker as symbol,
    split_to,
    split_from,
    execution_date
from {{ source('polygon','stock_split')}}