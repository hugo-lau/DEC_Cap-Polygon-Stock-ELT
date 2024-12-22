select
    code,
    locale,
    asset_class,
    description
from {{ source('polygon','ticker_types')}}