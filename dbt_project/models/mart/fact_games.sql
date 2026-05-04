with events as (
    select * from {{ ref('stg_seatgeek_events') }}
),

dates as (
    select * from {{ ref('dim_dates') }}
)

select
    e.event_id as game_id,
    e.title,
    e.short_title,
    e.datetime_utc,
    e.datetime_local,
    d.date_id,
    e.venue_id,
    e.home_team_id,
    e.away_team_id,
    e.event_score,
    e.event_popularity,
    e.season_stage,
    e.game_number,
    e.home_game_number,
    e.status,
    e.event_url,
    e.stats_lowest_price,
    e.stats_average_price,
    e.stats_highest_price,
    e.stats_listing_count,
    e.date_tbd,
    e.time_tbd
from events e
left join dates d
    on cast(e.datetime_local as date) = d.date_day
