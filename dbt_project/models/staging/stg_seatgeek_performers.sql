with source as (
    select * from {{ source('raw', 'seatgeek_performers') }}
),

staged as (
    select
        id as team_id,
        name as team_name,
        short_name,
        slug,
        type,
        score as team_score,
        popularity as team_popularity,
        home_venue_id,
        division_conference as conference,
        division_division as division,
        image_url,
        url as team_url,
        _loaded_at
    from source
    where type = 'nhl'
      and home_venue_id is not null
)

select * from staged
