with source as (
    select * from {{ source('raw', 'seatgeek_venues') }}
),

staged as (
    select
        id as venue_id,
        name as venue_name,
        address,
        extended_address,
        city,
        state,
        country,
        postal_code,
        coalesce(capacity, 0) as capacity,
        score as venue_score,
        popularity as venue_popularity,
        latitude,
        longitude,
        url as venue_url,
        _loaded_at
    from source
)

select * from staged
