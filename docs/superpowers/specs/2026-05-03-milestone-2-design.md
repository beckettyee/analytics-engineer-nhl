# Milestone 2 Design Spec: Present & Polish

**Date:** 2026-05-03
**Scope:** dbt project (staging + mart), Source 2 Snowflake load, Streamlit dashboard, knowledge base wiki, README, ERD, pipeline diagram

## Overview

Milestone 2 transforms raw data into a star schema via dbt, builds an interactive Streamlit dashboard connected to mart tables, generates a knowledge base wiki from scraped sources, and polishes the repo with README, ERD, and pipeline diagram.

## Sub-project A: dbt Project

### Project Location

`dbt_project/`

### Layer Pattern

raw → staging → mart

### Staging Models

| Model | Source | Purpose |
|---|---|---|
| `stg_seatgeek_events` | `raw.seatgeek_events` | Cast timestamps, rename fields, filter to valid events |
| `stg_seatgeek_performers` | `raw.seatgeek_performers` | Filter to actual NHL teams (exclude "NHL Draft", "NHL Eastern Conference Finals", etc.), clean fields |
| `stg_seatgeek_venues` | `raw.seatgeek_venues` | Clean fields, handle nulls in capacity |

### Mart Models (Star Schema)

| Model | Source | Key | Description |
|---|---|---|---|
| `fact_games` | `stg_seatgeek_events` | `game_id` | One row per NHL game/event. FKs to dim_teams (home_team_id, away_team_id), dim_dates (date_id), dim_venues (venue_id). Measures: score, popularity, stats_lowest_price, stats_average_price, stats_highest_price, stats_listing_count |
| `dim_teams` | `stg_seatgeek_performers` | `team_id` | One row per NHL team. conference, division, popularity, score, home_venue_id |
| `dim_dates` | Generated from game dates | `date_id` | date, day_of_week, day_name, month, month_name, year, is_weekend, is_playoff_month |
| `dim_venues` | `stg_seatgeek_venues` | `venue_id` | name, city, state, country, capacity, latitude, longitude |

### dbt Tests

- `not_null` on all primary keys and critical FKs
- `unique` on all primary keys
- `relationships` between fact_games and each dimension
- `accepted_values` on season_stage (postseason, null)

### dbt Profile

Connects to Snowflake NHL_ANALYTICS database using key pair auth. Profile configured in `dbt_project/profiles.yml` (gitignored) with env vars.

## Sub-project B: Source 2 Load to Snowflake

### New Raw Table

`raw.scraped_documents`
- `filename` VARCHAR (PK)
- `url` VARCHAR
- `content` VARCHAR (full markdown text)
- `_loaded_at` TIMESTAMP_NTZ

### Script

`extract/load_scraped_docs.py` — reads markdown files from `knowledge/raw/` and the URL mapping from `extract/scrape_urls.yaml`, upserts into Snowflake `raw.scraped_documents`.

### GitHub Actions

Add as a step in the `firecrawl-scrape` job, after the scrape step and before the git commit step.

## Sub-project C: Streamlit Dashboard

### Location

`streamlit/app.py`

### Connection

Connects to Snowflake mart tables using key pair auth via `snowflake-connector-python`.

### Layout — 3 Tabs

**Tab 1: Schedule Overview (descriptive)**
- Table/chart of all NHL games
- Filters: team selector, date range, venue
- Visuals: game count by team, games by month

**Tab 2: Demand Analysis (diagnostic)**
- Why are some games more popular?
- Scatter/bar charts: popularity by team, venue, day of week, playoff vs other
- Answers "what drives event demand?"

**Tab 3: Pricing Intelligence (diagnostic)**
- Ticket pricing analysis for events with pricing data
- Price distribution, price vs popularity correlation
- Graceful handling if pricing data is sparse

### Interactive Elements

- Team selector (multiselect)
- Date range filter
- Season stage filter (postseason / all)
- Venue filter

### Deployment

Streamlit Community Cloud, public URL. Requires `streamlit/requirements.txt` and `streamlit/.streamlit/secrets.toml` (gitignored).

## Sub-project D: Knowledge Base

### Wiki Pages (`knowledge/wiki/`)

| Page | Content |
|---|---|
| `overview.md` | Project domain overview: LA Kings, AEG, NHL ticketing landscape |
| `key-entities.md` | Key organizations and entities: AEG, Crypto.com Arena, SeatGeek, Ticketmaster, StubHub |
| `dynamic-pricing-insights.md` | Synthesis of dynamic pricing strategies across sources |

### Index

`knowledge/index.md` — lists all wiki pages with one-line summaries.

### CLAUDE.md Update

Add a section explaining how to query the knowledge base (read wiki pages and raw sources to answer questions).

## Sub-project E: Polish

### ERD

Mermaid diagram showing fact_games + dim_teams + dim_dates + dim_venues with relationships and key columns. Included in README.

### Pipeline Diagram

Mermaid flowchart showing full data flow:
- SeatGeek API → GitHub Actions → Snowflake RAW → dbt Staging → dbt Mart → Streamlit Dashboard
- Firecrawl → GitHub Actions → knowledge/raw/ → Claude Code → knowledge/wiki/

Included in README.

### README.md

From project template. Sections: project overview, tech stack, data pipeline diagram, ERD, setup/reproduction instructions, insights summary.

### Slides

PDF created separately (not built in code). Deliverable to Brightspace, not in repo pipeline.
