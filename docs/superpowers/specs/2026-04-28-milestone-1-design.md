# Milestone 1 Design Spec: Extract, Load & Scrape

**Date:** 2026-04-28
**Scope:** Source 1 (API) extraction + load to Snowflake raw, Source 2 (web scrape) to knowledge/raw/, Snowflake account setup, GitHub Actions automation

## Overview

Milestone 1 delivers the data extraction layer for the NHL Opponent & Schedule Intelligence Tool. Two Python scripts extract data from the SeatGeek API and web sources via Firecrawl, loading structured data into Snowflake and unstructured content into the repo's knowledge base. Both are automated via a single GitHub Actions workflow.

## Source 1: SeatGeek API Extract + Load

### Script

`extract/seatgeek_extract.py`

### Endpoints

| Endpoint | Filter | Purpose |
|---|---|---|
| `/events` | `performers.slug=los-angeles-kings` | LA Kings games (home + away), paginated |
| `/performers` | Kings + opponent teams from events | Team metadata |
| `/venues` | Venues referenced by Kings events | Arena info |

**Note:** Scoped to LA Kings for now. Can expand to all NHL events later by removing the performer filter.

### Snowflake Raw Tables

| Table | Source | Key |
|---|---|---|
| `raw.seatgeek_events` | `/events` response | `id` |
| `raw.seatgeek_performers` | `/performers` response | `id` |
| `raw.seatgeek_venues` | `/venues` response | `id` |

### Load Strategy

- Flatten JSON response fields into columns (not raw JSON blobs)
- Upsert on `id` to prevent duplicates on reruns
- Connection via `snowflake-connector-python`

### Key Event Fields

From the API (documented + undocumented):
- `id`, `title`, `short_title`, `datetime_utc`, `datetime_local`
- `score`, `popularity`, `season_stage`, `game_number`, `home_game_number`
- `stats` (pricing data when available: lowest_price, average_price, highest_price, listing_count)
- `venue.id`, performer IDs (home_team, away_team)
- `type`, `date_tbd`, `time_tbd`, `announce_date`, `visible_until`

### Key Performer Fields

- `id`, `name`, `short_name`, `slug`, `type`
- `score`, `popularity`, `home_venue_id`
- `divisions` (conference, division)
- `colors`, `images`

### Key Venue Fields

- `id`, `name`, `address`, `city`, `state`, `country`, `postal_code`
- `capacity`, `score`, `popularity`
- `location.lat`, `location.lon`

## Source 2: Firecrawl Web Scrape

### Script

`extract/firecrawl_scrape.py`

### Content Themes

1. **LA Kings / AEG** — team pages, press releases, arena info, leadership bios
2. **Ticket pricing industry** — dynamic pricing articles, demand-driven strategies in sports

### How It Works

- Curated URL list stored in `extract/scrape_urls.yaml`
- Calls Firecrawl API to scrape each URL, returns markdown
- Saves each page as a markdown file in `knowledge/raw/` with a descriptive filename
- Skips URLs already scraped (file exists check) to avoid duplicates on reruns
- Target: 15+ sources from 3+ different sites/authors

### Credentials

- `FIRECRAWL_API_KEY` env var

## Snowflake Setup

| Component | Value |
|---|---|
| Database | `NHL_ANALYTICS` |
| Schemas | `RAW`, `STAGING`, `MART` |
| Warehouse | `COMPUTE_WH` (XS) |
| Region | AWS US East 1 |

Raw tables are created by the extract script on first run (CREATE TABLE IF NOT EXISTS).

## GitHub Actions

### Workflow

`.github/workflows/extract_load.yml`

### Triggers

- `schedule:` — daily cron (6 AM UTC)
- `workflow_dispatch:` — manual trigger

### Jobs

1. **seatgeek-extract** — install deps from `requirements.txt`, run `extract/seatgeek_extract.py`
2. **firecrawl-scrape** — run `extract/firecrawl_scrape.py`, commit any new `knowledge/raw/` files back to the repo

### Secrets (GitHub repo settings)

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_WAREHOUSE`
- `SEATGEEK_CLIENT_ID`
- `FIRECRAWL_API_KEY`

### Dependencies

`requirements.txt`:
- `snowflake-connector-python`
- `requests`
- `firecrawl-py`
- `pyyaml`

## Design Decisions

1. **SeatGeek over NHL API for Source 1** — SeatGeek provides event + ticket data in one source, which is core to the pricing analysis use case. NHL API can be added later for richer game stats.
2. **Firecrawl Python API for scraping** — automatable via GitHub Actions, unlike MCP which is interactive-only. Consistent with the "both sources automated" approach.
3. **Upsert strategy** — prevents duplicate rows on reruns without needing to truncate/reload.
4. **Flat columns over JSON blobs** — makes downstream dbt staging models simpler and Snowflake queries more performant.
5. **URL config in YAML** — easy to add new scrape targets without modifying Python code.
