select
    id,
    mic,
    url,
    name,
    type,
    locale,
    acronym,
    asset_class,
    operating_mic,
    participant_id
from {{ source('polygon','exchanges')}}