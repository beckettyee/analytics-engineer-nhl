with venues as (
    select * from {{ ref('stg_seatgeek_venues') }}
)

select
    venue_id,
    venue_name,
    address,
    city,
    state,
    country,
    postal_code,
    capacity,
    venue_score,
    venue_popularity,
    latitude,
    longitude,
    venue_url
from venues
