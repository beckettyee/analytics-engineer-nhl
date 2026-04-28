"""Extract LA Kings data from SeatGeek API and load to Snowflake raw tables."""

import os
import requests
import snowflake.connector

BASE_URL = "https://api.seatgeek.com/2"
KINGS_SLUG = "los-angeles-kings"


def get_seatgeek_client_id():
    return os.environ["SEATGEEK_CLIENT_ID"]


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ.get("SNOWFLAKE_DATABASE", "NHL_ANALYTICS"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        schema="RAW",
    )


def fetch_events(client_id):
    """Fetch all LA Kings events, paginating through results."""
    events = []
    page = 1
    per_page = 100
    while True:
        resp = requests.get(
            f"{BASE_URL}/events",
            params={
                "performers.slug": KINGS_SLUG,
                "per_page": per_page,
                "page": page,
                "client_id": client_id,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("events", [])
        if not batch:
            break
        events.extend(batch)
        total = data.get("meta", {}).get("total", 0)
        if page * per_page >= total:
            break
        page += 1
    print(f"Fetched {len(events)} events")
    return events


def extract_performer_ids(events):
    """Get unique performer IDs from all events."""
    performer_ids = set()
    for event in events:
        for performer in event.get("performers", []):
            performer_ids.add(performer["id"])
    return performer_ids


def fetch_performers(client_id, performer_ids):
    """Fetch performer details by ID."""
    if not performer_ids:
        print("Fetched 0 performers")
        return []
    performers = []
    id_list = ",".join(str(pid) for pid in performer_ids)
    resp = requests.get(
        f"{BASE_URL}/performers",
        params={"id": id_list, "client_id": client_id},
    )
    resp.raise_for_status()
    performers = resp.json().get("performers", [])
    print(f"Fetched {len(performers)} performers")
    return performers


def extract_venue_ids(events):
    """Get unique venue IDs from all events."""
    return {event["venue"]["id"] for event in events if event.get("venue")}


def fetch_venues(client_id, venue_ids):
    """Fetch venue details by ID."""
    if not venue_ids:
        print("Fetched 0 venues")
        return []
    id_list = ",".join(str(vid) for vid in venue_ids)
    resp = requests.get(
        f"{BASE_URL}/venues",
        params={"id": id_list, "client_id": client_id},
    )
    resp.raise_for_status()
    venues = resp.json().get("venues", [])
    print(f"Fetched {len(venues)} venues")
    return venues


def parse_home_away(event):
    """Extract home and away team performer IDs from an event."""
    home_id = None
    away_id = None
    for performer in event.get("performers", []):
        if performer.get("home_team"):
            home_id = performer["id"]
        elif performer.get("away_team"):
            away_id = performer["id"]
    return home_id, away_id


def load_events(conn, events):
    """Upsert events into Snowflake raw.seatgeek_events."""
    cur = conn.cursor()
    for event in events:
        stats = event.get("stats", {}) or {}
        home_id, away_id = parse_home_away(event)
        cur.execute("""
            MERGE INTO seatgeek_events t
            USING (SELECT %(id)s AS id) s ON t.id = s.id
            WHEN MATCHED THEN UPDATE SET
                title = %(title)s,
                short_title = %(short_title)s,
                datetime_utc = %(datetime_utc)s,
                datetime_local = %(datetime_local)s,
                announce_date = %(announce_date)s,
                visible_until = %(visible_until)s,
                date_tbd = %(date_tbd)s,
                time_tbd = %(time_tbd)s,
                datetime_tbd = %(datetime_tbd)s,
                type = %(type)s,
                score = %(score)s,
                popularity = %(popularity)s,
                season_stage = %(season_stage)s,
                game_number = %(game_number)s,
                home_game_number = %(home_game_number)s,
                status = %(status)s,
                url = %(url)s,
                venue_id = %(venue_id)s,
                home_team_id = %(home_team_id)s,
                away_team_id = %(away_team_id)s,
                stats_lowest_price = %(stats_lowest_price)s,
                stats_average_price = %(stats_average_price)s,
                stats_highest_price = %(stats_highest_price)s,
                stats_listing_count = %(stats_listing_count)s,
                _loaded_at = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN INSERT (
                id, title, short_title, datetime_utc, datetime_local,
                announce_date, visible_until, date_tbd, time_tbd, datetime_tbd,
                type, score, popularity, season_stage, game_number,
                home_game_number, status, url, venue_id,
                home_team_id, away_team_id,
                stats_lowest_price, stats_average_price,
                stats_highest_price, stats_listing_count
            ) VALUES (
                %(id)s, %(title)s, %(short_title)s, %(datetime_utc)s, %(datetime_local)s,
                %(announce_date)s, %(visible_until)s, %(date_tbd)s, %(time_tbd)s, %(datetime_tbd)s,
                %(type)s, %(score)s, %(popularity)s, %(season_stage)s, %(game_number)s,
                %(home_game_number)s, %(status)s, %(url)s, %(venue_id)s,
                %(home_team_id)s, %(away_team_id)s,
                %(stats_lowest_price)s, %(stats_average_price)s,
                %(stats_highest_price)s, %(stats_listing_count)s
            )
        """, {
            "id": event["id"],
            "title": event.get("title"),
            "short_title": event.get("short_title"),
            "datetime_utc": event.get("datetime_utc"),
            "datetime_local": event.get("datetime_local"),
            "announce_date": event.get("announce_date"),
            "visible_until": event.get("visible_until_utc"),
            "date_tbd": event.get("date_tbd"),
            "time_tbd": event.get("time_tbd"),
            "datetime_tbd": event.get("datetime_tbd"),
            "type": event.get("type"),
            "score": event.get("score"),
            "popularity": event.get("popularity"),
            "season_stage": event.get("season_stage"),
            "game_number": event.get("game_number"),
            "home_game_number": event.get("home_game_number"),
            "status": event.get("status"),
            "url": event.get("url"),
            "venue_id": event.get("venue", {}).get("id"),
            "home_team_id": home_id,
            "away_team_id": away_id,
            "stats_lowest_price": stats.get("lowest_price"),
            "stats_average_price": stats.get("average_price"),
            "stats_highest_price": stats.get("highest_price"),
            "stats_listing_count": stats.get("listing_count"),
        })
    print(f"Loaded {len(events)} events")
    cur.close()


def load_performers(conn, performers):
    """Upsert performers into Snowflake raw.seatgeek_performers."""
    cur = conn.cursor()
    for p in performers:
        divisions = p.get("divisions", [])
        conference = None
        division = None
        for d in divisions:
            if d.get("display_type") == "Conference":
                conference = d.get("display_name")
            elif d.get("display_type") == "Division":
                division = d.get("display_name")

        cur.execute("""
            MERGE INTO seatgeek_performers t
            USING (SELECT %(id)s AS id) s ON t.id = s.id
            WHEN MATCHED THEN UPDATE SET
                name = %(name)s,
                short_name = %(short_name)s,
                slug = %(slug)s,
                type = %(type)s,
                score = %(score)s,
                popularity = %(popularity)s,
                home_venue_id = %(home_venue_id)s,
                division_conference = %(division_conference)s,
                division_division = %(division_division)s,
                image_url = %(image_url)s,
                url = %(url)s,
                _loaded_at = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN INSERT (
                id, name, short_name, slug, type, score, popularity,
                home_venue_id, division_conference, division_division,
                image_url, url
            ) VALUES (
                %(id)s, %(name)s, %(short_name)s, %(slug)s, %(type)s,
                %(score)s, %(popularity)s, %(home_venue_id)s,
                %(division_conference)s, %(division_division)s,
                %(image_url)s, %(url)s
            )
        """, {
            "id": p["id"],
            "name": p.get("name"),
            "short_name": p.get("short_name"),
            "slug": p.get("slug"),
            "type": p.get("type"),
            "score": p.get("score"),
            "popularity": p.get("popularity"),
            "home_venue_id": p.get("home_venue_id"),
            "division_conference": conference,
            "division_division": division,
            "image_url": p.get("image"),
            "url": p.get("url"),
        })
    print(f"Loaded {len(performers)} performers")
    cur.close()


def load_venues(conn, venues):
    """Upsert venues into Snowflake raw.seatgeek_venues."""
    cur = conn.cursor()
    for v in venues:
        location = v.get("location", {}) or {}
        cur.execute("""
            MERGE INTO seatgeek_venues t
            USING (SELECT %(id)s AS id) s ON t.id = s.id
            WHEN MATCHED THEN UPDATE SET
                name = %(name)s,
                address = %(address)s,
                extended_address = %(extended_address)s,
                city = %(city)s,
                state = %(state)s,
                country = %(country)s,
                postal_code = %(postal_code)s,
                capacity = %(capacity)s,
                score = %(score)s,
                popularity = %(popularity)s,
                latitude = %(latitude)s,
                longitude = %(longitude)s,
                url = %(url)s,
                _loaded_at = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN INSERT (
                id, name, address, extended_address, city, state, country,
                postal_code, capacity, score, popularity, latitude, longitude, url
            ) VALUES (
                %(id)s, %(name)s, %(address)s, %(extended_address)s,
                %(city)s, %(state)s, %(country)s, %(postal_code)s,
                %(capacity)s, %(score)s, %(popularity)s,
                %(latitude)s, %(longitude)s, %(url)s
            )
        """, {
            "id": v["id"],
            "name": v.get("name"),
            "address": v.get("address"),
            "extended_address": v.get("extended_address"),
            "city": v.get("city"),
            "state": v.get("state"),
            "country": v.get("country"),
            "postal_code": v.get("postal_code"),
            "capacity": v.get("capacity"),
            "score": v.get("score"),
            "popularity": v.get("popularity"),
            "latitude": location.get("lat"),
            "longitude": location.get("lon"),
            "url": v.get("url"),
        })
    print(f"Loaded {len(venues)} venues")
    cur.close()


def main():
    client_id = get_seatgeek_client_id()
    conn = get_snowflake_connection()

    events = fetch_events(client_id)
    performer_ids = extract_performer_ids(events)
    venue_ids = extract_venue_ids(events)

    performers = fetch_performers(client_id, performer_ids)
    venues = fetch_venues(client_id, venue_ids)

    load_events(conn, events)
    load_performers(conn, performers)
    load_venues(conn, venues)

    conn.close()
    print("SeatGeek extract + load complete.")


if __name__ == "__main__":
    main()
