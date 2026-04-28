"""One-time Snowflake setup: creates database, schemas, and raw tables."""

import os
import snowflake.connector


def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    )


def setup_snowflake():
    conn = get_connection()
    cur = conn.cursor()

    database = os.environ.get("SNOWFLAKE_DATABASE", "NHL_ANALYTICS")

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cur.execute(f"USE DATABASE {database}")

    for schema in ("RAW", "STAGING", "MART"):
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

    cur.execute(f"USE SCHEMA RAW")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS seatgeek_events (
            id INTEGER PRIMARY KEY,
            title VARCHAR,
            short_title VARCHAR,
            datetime_utc TIMESTAMP_NTZ,
            datetime_local TIMESTAMP_NTZ,
            announce_date TIMESTAMP_NTZ,
            visible_until TIMESTAMP_NTZ,
            date_tbd BOOLEAN,
            time_tbd BOOLEAN,
            datetime_tbd BOOLEAN,
            type VARCHAR,
            score FLOAT,
            popularity FLOAT,
            season_stage VARCHAR,
            game_number INTEGER,
            home_game_number INTEGER,
            status VARCHAR,
            url VARCHAR,
            venue_id INTEGER,
            home_team_id INTEGER,
            away_team_id INTEGER,
            stats_lowest_price FLOAT,
            stats_average_price FLOAT,
            stats_highest_price FLOAT,
            stats_listing_count INTEGER,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS seatgeek_performers (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            short_name VARCHAR,
            slug VARCHAR,
            type VARCHAR,
            score FLOAT,
            popularity FLOAT,
            home_venue_id INTEGER,
            division_conference VARCHAR,
            division_division VARCHAR,
            image_url VARCHAR,
            url VARCHAR,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS seatgeek_venues (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            address VARCHAR,
            extended_address VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR,
            postal_code VARCHAR,
            capacity INTEGER,
            score FLOAT,
            popularity FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            url VARCHAR,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)

    print(f"Setup complete: {database} with RAW, STAGING, MART schemas and raw tables.")
    cur.close()
    conn.close()


if __name__ == "__main__":
    setup_snowflake()
