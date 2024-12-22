select
    {{dbt_utils.generate_surrogate_key(['e.name']) }} as exchanage_key,
    e.id,
    e.asset_class,
    e.mic,
    e.name as exchange_name,
    e.type as exchange_type,
    e.locale,
    e.operating_mic
from {{ ref('exchanges') }} as e