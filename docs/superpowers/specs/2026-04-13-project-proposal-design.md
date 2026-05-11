# Project Proposal Design Spec

## Overview

**Project**: NHL Opponent & Schedule Intelligence Tool for Ticket Pricing

**Target Job**: LA Kings - Sr. Data Analyst (AEG, El Segundo, CA) — focused on dynamic pricing strategy for ticketing, revenue optimization, and demand forecasting.

**Framing**: Build a data pipeline and analytics tool that a sports pricing team would use to understand historical demand drivers — opponent strength, scheduling patterns, team performance trends, and actual ticket pricing — to inform dynamic ticket pricing decisions.

## Data Sources

### Source 1: NHL Public Stats API (Structured)
- Game results, team standings, schedules, player stats across multiple seasons
- Feeds the structured data pipeline (Snowflake → dbt → Streamlit)

### Source 2: SeatGeek API (Structured)
- Ticket listings, pricing data (min/avg/max), event popularity metrics for LA Kings games
- Feeds the structured data pipeline alongside NHL API data
- Provides actual demand/pricing signals for the star schema

### Source 3: Web Scrape (Unstructured)
- Sports business articles: dynamic pricing in sports, ticket market trends, AEG/Kings business news
- LA Kings team news, player profiles, analyst commentary
- Feeds the knowledge base (knowledge/raw/ → knowledge/wiki/)

## Star Schema

### Fact Table
- `fact_games` — one row per game: scores, shots, power plays, home/away, win/loss, overtime flag, ticket pricing metrics (min/avg/max price, listing count from SeatGeek)

### Dimension Tables
- `dim_teams` — team attributes, conference, division, season win/loss/points
- `dim_dates` — date, day of week, month, weekend flag, holiday flag, time of day
- `dim_opponents` — opponent strength metrics (points %, recent form, rivalry flag)
- `dim_seasons` — season-level context
- `dim_venues` — arena info for home/away game pricing comparison

## Pipeline Architecture

```
NHL API ──┐
           ├→ Python extract scripts → Snowflake Raw → dbt Staging → dbt Mart (star schema) → Streamlit Dashboard
SeatGeek ──┘

Web Scrape → Python scrape script → knowledge/raw/ → Claude Code → knowledge/wiki/

Both paths automated via GitHub Actions on cron schedule + manual trigger
```

### Layers
- **Extract/Load**: Python scripts using `requests` for NHL API and SeatGeek API. Web scraping library (beautifulsoup4 or Firecrawl) for articles. Structured data loads to Snowflake raw schema. Unstructured data saves to `knowledge/raw/` in repo.
- **Transform**: dbt project: raw → staging (clean, rename, cast) → mart (star schema joins, calculated fields like opponent strength metrics)
- **Serve**: Streamlit app connected to Snowflake mart tables, deployed to Streamlit Community Cloud
- **Orchestration**: GitHub Actions workflows — one for API extract+load, one for web scrape. Both on cron schedule + manual trigger.
- **Secrets**: Snowflake credentials and API keys stored as GitHub Actions secrets + local `.env` (gitignored)

## Streamlit Dashboard

### Descriptive View ("What happened?")
- Season performance overview
- Home game outcomes
- Opponent breakdown
- Ticket price trends over the season

### Diagnostic View ("Why did it happen?")
- Demand driver analysis: which factors (day of week, opponent strength, streaks, rivalry games) correlate with higher ticket prices
- Price variation by opponent, schedule slot, team performance

### Interactive Elements
- Filter by season, opponent, date range, game type
- Selectors for comparing metrics

## Knowledge Base

- `knowledge/raw/` — 15+ scraped sources from 3+ sites (sports business publications, AEG press releases, Kings news outlets, industry reports)
- `knowledge/wiki/` — Claude Code-generated synthesis pages:
  - Overview of sports ticket pricing industry
  - Key entities (AEG, Kings, competitors, pricing platforms)
  - Pricing themes and trends synthesis
- `knowledge/index.md` — index of all wiki pages
- Queryable via Claude Code against the repo

## Directory Structure

```
analytics-engineer-nhl/
├── CLAUDE.md
├── .gitignore
├── docs/
│   ├── job-posting.pdf
│   └── proposal.md
├── extract/              # Python extract/load scripts
├── dbt_project/          # dbt models
├── streamlit/            # Streamlit dashboard app
├── knowledge/            # Knowledge base
│   ├── raw/
│   └── wiki/
└── .github/workflows/    # GitHub Actions
```

## Proposal Deliverables (Due Apr 13)

1. `docs/job-posting.pdf` — LA Kings Sr. Data Analyst posting (already in repo, needs rename from job-description.pdf)
2. `docs/proposal.md` — one-page proposal using template, with reflection connecting job skills to coursework
3. Repo setup — `.gitignore`, directory structure, `CLAUDE.md` with project context
