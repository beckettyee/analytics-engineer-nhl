with source as (
    select * from {{ source('raw', 'seatgeek_events') }}
),

staged as (
    select
        id as event_id,
        title,
        short_title,
        datetime_utc,
        datetime_local,
        announce_date,
        visible_until,
        date_tbd,
        time_tbd,
        datetime_tbd,
        type,
        score as event_score,
        popularity as event_popularity,
        season_stage,
        game_number,
        home_game_number,
        status,
        url as event_url,
        venue_id,
        home_team_id,
        away_team_id,
        stats_lowest_price,
        stats_average_price,
        stats_highest_price,
        stats_listing_count,
        _loaded_at
    from source
    where type = 'nhl'
)

select * from staged
