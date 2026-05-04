with teams as (
    select * from {{ ref('stg_seatgeek_performers') }}
)

select
    team_id,
    team_name,
    short_name,
    slug,
    conference,
    division,
    team_score,
    team_popularity,
    home_venue_id,
    image_url,
    team_url
from teams
