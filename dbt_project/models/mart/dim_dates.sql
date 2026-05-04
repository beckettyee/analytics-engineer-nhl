with event_dates as (
    select distinct
        cast(datetime_local as date) as date_day
    from {{ ref('stg_seatgeek_events') }}
    where datetime_local is not null
)

select
    to_number(to_char(date_day, 'YYYYMMDD')) as date_id,
    date_day,
    dayofweek(date_day) as day_of_week,
    dayname(date_day) as day_name,
    month(date_day) as month_number,
    monthname(date_day) as month_name,
    year(date_day) as year,
    case when dayofweek(date_day) in (0, 6) then true else false end as is_weekend,
    case when month(date_day) in (4, 5, 6) then true else false end as is_playoff_month
from event_dates
