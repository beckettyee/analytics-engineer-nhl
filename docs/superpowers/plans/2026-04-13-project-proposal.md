



# Project Proposal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the project proposal deliverables — job posting PDF (renamed), proposal markdown with reflection, and repo setup (CLAUDE.md, directory structure).

**Architecture:** Three independent deliverables that can be completed in sequence. The proposal markdown follows the provided template. CLAUDE.md establishes project context for future Claude Code sessions.

**Tech Stack:** Markdown, Git

---

### Task 1: Rename job posting PDF

**Files:**
- Rename: `docs/job-description.pdf` → `docs/job-posting.pdf`

- [ ] **Step 1: Rename the file**

```bash
cd /Users/beckettyee/Github/analytics-engineer-nhl
git mv docs/job-description.pdf docs/job-posting.pdf
```

- [ ] **Step 2: Commit**

```bash
git add docs/job-posting.pdf
git commit -m "docs: rename job-description.pdf to job-posting.pdf per project requirements"
```

---

### Task 2: Write proposal markdown

**Files:**
- Create: `docs/proposal.md`
- Reference: `docs/proposal-template.md` (template to follow)

- [ ] **Step 1: Create `docs/proposal.md` using the template structure**

The proposal must follow the exact template outline from `docs/proposal-template.md`:

```markdown
# Project Proposal

**Name:** Beckett Yee

**Project Name:** analytics-engineer-nhl

**GitHub Repo:** https://github.com/beckettyee/analytics-engineer-nhl

## Job Posting

- **Role:** Sr. Data Analyst
- **Company:** Los Angeles Kings (AEG)
- **Link:** [Original posting URL — user to fill in if available]

**SQL requirement (quote the posting):** "Expertise in SQL, statistical programming (Python) and Spark" and "Build and maintain SQL-based views across data warehouses, ensuring suitability for reporting, accuracy, performance, and data integrity."

## Reflection

This posting is directly relevant to this class because the Sr. Data Analyst role at the LA Kings requires building SQL-based views across data warehouses, optimizing data pipelines with a Data Engineering team, and communicating analytical findings to leadership — all core skills practiced through dbt, Snowflake, and GitHub Actions in this course. The role specifically demands expertise in SQL, Python, and data modeling to drive dynamic pricing strategy, which maps to the dimensional modeling, staging/mart transformations, and Streamlit dashboarding we've built throughout the semester. To prove I can do this job, I'll build an NHL Opponent & Schedule Intelligence Tool that combines game stats from the NHL API and ticket pricing data from the SeatGeek API into a star schema, then surfaces demand-driver analysis through an interactive Streamlit dashboard — the kind of tool a pricing team would actually use to understand how opponent strength, scheduling, and team performance affect ticket demand. This project transfers directly to similar roles like Data Analyst at other professional sports franchises (NBA, MLB, MLS), Pricing Analyst at live entertainment or ticketing companies (Ticketmaster, StubHub, Live Nation), or Business Intelligence Analyst at venue management organizations like AEG or Oak View Group.
```

- [ ] **Step 2: Verify the proposal covers all template requirements**

Check that `docs/proposal.md` contains:
- Name, Project Name, GitHub Repo link
- Job Posting section with Role, Company, Link
- SQL requirement quoted from the posting
- Reflection paragraph (4-6 sentences) that answers: (1) why relevant to class, (2) which coursework skills, (3) what you'd build, (4) 2-3 transferable roles

- [ ] **Step 3: Commit**

```bash
git add docs/proposal.md
git commit -m "docs: add project proposal with reflection for LA Kings Sr. Data Analyst role"
```

---

### Task 3: Create CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Create `CLAUDE.md` with project context**

```markdown
# CLAUDE.md

## Project Overview

NHL Opponent & Schedule Intelligence Tool for Ticket Pricing. This project builds an end-to-end data pipeline and analytics tool targeting the LA Kings Sr. Data Analyst role (AEG). It demonstrates SQL, data pipelines, dimensional modeling, and demand/pricing analysis skills.

## Tech Stack

- **Data Warehouse:** Snowflake (AWS US East 1)
- **Transformation:** dbt
- **Orchestration:** GitHub Actions
- **Dashboard:** Streamlit (deployed to Streamlit Community Cloud)
- **Languages:** Python, SQL

## Data Sources

1. **NHL API** — game results, team standings, schedules, player stats
2. **SeatGeek API** — ticket listings, pricing data (min/avg/max), event popularity
3. **Web scrape** — sports business articles, AEG/Kings news (feeds knowledge base)

## Project Structure

```
analytics-engineer-nhl/
├── CLAUDE.md
├── .gitignore
├── docs/                  # Proposal, job posting, specs, plans
├── extract/               # Python extract/load scripts
├── dbt_project/           # dbt models (staging + mart)
├── streamlit/             # Streamlit dashboard app
├── knowledge/             # Knowledge base
│   ├── raw/               # Scraped source documents
│   └── wiki/              # Claude Code-generated synthesis pages
└── .github/workflows/     # GitHub Actions pipelines
```

## Star Schema

- `fact_games` — game stats + ticket pricing metrics per game
- `dim_teams` — team attributes, conference, division, season record
- `dim_dates` — date, day of week, weekend/holiday flags
- `dim_opponents` — opponent strength metrics, rivalry flag
- `dim_seasons` — season-level context
- `dim_venues` — arena info

## Conventions

- Environment variables for all secrets (Snowflake creds, API keys) — never commit credentials
- `.env` files are gitignored
- dbt models follow raw → staging → mart layer pattern

## Knowledge Base

The `knowledge/` folder contains a queryable knowledge base:
- `knowledge/raw/` — scraped source documents (15+ from 3+ sites)
- `knowledge/wiki/` — synthesized wiki pages generated by Claude Code
- `knowledge/index.md` — index of all wiki pages

To query the knowledge base, read the relevant wiki pages and raw sources in `knowledge/` to answer questions about the sports ticketing industry, LA Kings, AEG, and dynamic pricing trends.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project context and conventions"
```

---

### Task 4: Set up directory structure

**Files:**
- Create directories: `extract/`, `dbt_project/`, `streamlit/`, `knowledge/raw/`, `knowledge/wiki/`, `.github/workflows/`
- Create: `.gitkeep` files in each empty directory

- [ ] **Step 1: Create all directories with .gitkeep files**

```bash
mkdir -p extract dbt_project streamlit knowledge/raw knowledge/wiki .github/workflows
touch extract/.gitkeep dbt_project/.gitkeep streamlit/.gitkeep knowledge/raw/.gitkeep knowledge/wiki/.gitkeep .github/workflows/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add extract/ dbt_project/ streamlit/ knowledge/ .github/
git commit -m "chore: scaffold project directory structure"
```

---

### Task 5: Update .gitignore

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add project-specific entries to `.gitignore`**

Add these lines to the end of the existing `.gitignore`:

```
# Snowflake credentials
.env
.env.*

# dbt
dbt_project/target/
dbt_project/dbt_packages/
dbt_project/logs/

# Streamlit
streamlit/.streamlit/secrets.toml
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: add dbt, Streamlit, and Snowflake entries to .gitignore"
```
