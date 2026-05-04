# Key Entities Reference

This page provides concise reference profiles for the major organizations relevant to this project.

---

## AEG (Anschutz Entertainment Group)

**What it is:** The world's largest owner of sports teams and venues, and the second-largest live entertainment presenter globally (after Live Nation).

**Founded:** 1994 by Philip Anschutz
**HQ:** L.A. Live, Downtown Los Angeles
**CEO:** Dan Beckerman

**Key facts:**
- Hosts 100M+ guests annually at 13,000+ events across 100+ venues
- Sports portfolio: LA Kings (NHL), LA Galaxy (MLS), Ontario Reign (AHL), Eisbären Berlin (DEL)
- Venue portfolio: Crypto.com Arena (LA), Dignity Health Sports Park (LA), The O2 (London), Uber Arena (Berlin)
- Music/entertainment: AEG Presents (concert promotion arm), Goldenvoice, Coachella
- AEG Facilities merged with SMG in 2019 to form ASM Global
- DOJ required Live Nation to license Ticketmaster software to AEG as a condition of the 2010 Ticketmaster-Live Nation merger

**Project relevance:** AEG owns the LA Kings (the primary subject of this analysis) and Crypto.com Arena. AEG is the employer this project is targeting (LA Kings Sr. Data Analyst role). Understanding AEG's position as a major venue operator and team owner is critical context for why ticket pricing intelligence matters.

---

## Crypto.com Arena

**What it is:** An indoor arena in Downtown Los Angeles, home of the LA Kings and LA Lakers.

**Opened:** October 17, 1999 (as Staples Center)
**Renamed:** December 25, 2021
**Owner:** AEG
**Location:** 1111 S Figueroa Street, Los Angeles, CA

**Key facts:**
- 950,000 sq ft; capacity 18,145 for hockey, 19,079 for basketball, ~20,000 for concerts
- 160 luxury suites, 2,500 club seats
- Naming rights: $700M over 20 years with Crypto.com — the most valuable naming rights deal in sports history at time of signing
- Home of the Kings, Lakers, and WNBA's Sparks
- Hosted the 2012 and 2014 Stanley Cup Finals
- Has hosted the Grammy Awards 23 times
- Will host events during the 2028 Los Angeles Olympics

**Project relevance:** All LA Kings home game ticket pricing data in this project flows through events held at Crypto.com Arena. Venue capacity, suite inventory, and premium seating configuration influence the ticket supply side of pricing models.

---

## SeatGeek

**What it is:** A primary and secondary event ticketing platform, and the primary data source for this project.

**Founded:** September 2009 by Russell D'Souza and Jack Groetzinger (New York City)
**Business model:** Primary + secondary ticketing; marketplace aggregator
**Valuation:** ~$1B (Series E, 2022)
**Employees:** 800+

**Key facts:**
- Launched as a secondary market aggregator, expanded into primary ticketing in 2016 (starting with MLS)
- DealScore algorithm: proprietary seat value rating (1-100) to help buyers identify fair-priced listings
- Replaced Ticketmaster for the Dallas Cowboys in 2018
- NHL primary ticketing clients: Florida Panthers (2022), Utah Mammoth (2024)
- Official MLB marketplace: 2023
- AI-powered "Smart Pricing" tool for resellers launched February 2024
- Complies with FTC all-in pricing guidelines (no hidden fees at checkout)
- Raised $238M Series E (2022); investors include Accel, Causeway Media Partners, IVP

**Project relevance:** SeatGeek is the project's primary API data source. The SeatGeek API provides NHL event listings with ticket pricing data (min/avg/max prices), event popularity scores, and performer/venue metadata. SeatGeek's DealScore and pricing data allow analysis of demand patterns across the league.

---

## Ticketmaster

**What it is:** The dominant primary ticketing platform in North America, a subsidiary of Live Nation Entertainment.

**Founded:** October 2, 1976 in Phoenix, AZ
**Parent company:** Live Nation Entertainment (merger completed January 2010)
**HQ:** Beverly Hills, CA
**Revenue:** $23.16B (Live Nation, 2024)
**Employees:** ~6,678

**Key facts:**
- Controls primary ticketing for the majority of major venues and sports franchises in the US
- Merged with Live Nation in 2010 to form Live Nation Entertainment; DOJ approved the merger with conditions including licensing Ticketmaster software to AEG
- Introduced dynamic pricing across its platform in 2022, drawing widespread consumer criticism (Blink-182 tickets exceeded $600; Bruce Springsteen tickets reached $4,000-5,000)
- DOJ + 29 state attorneys general filed antitrust suit May 2024
- Jury found Live Nation Entertainment guilty of maintaining an illegal monopoly in April 2026

**Project relevance:** Ticketmaster is the dominant incumbent in NHL primary ticketing. Understanding Ticketmaster's market position, pricing practices, and regulatory challenges provides context for the competitive landscape SeatGeek operates in, and for why dynamic pricing analytics are a core business concern for teams and venue operators like AEG.

---

## StubHub

**What it is:** The largest secondary ticket marketplace in the United States.

**Founded:** March 2000 by Eric Baker and Jeff Fluhr in San Francisco
**Owner:** StubHub Holdings (majority owned by Viagogo, controlled by Eric Baker)
**Revenue:** $1.77B (2024)

**Key facts:**
- Sold to eBay in 2007 for $310M; acquired by Viagogo in 2020 for $4.05B
- StubHub Holdings IPO: September 2025 at an $8.6B valuation on Nasdaq
- Official ticket resale partner for AEG venues (partnership began 2012); also provides AXS integration
- DC Attorney General sued StubHub in 2024 for drip pricing (hiding fees until checkout)
- Operates as a marketplace (buyers + sellers) rather than a primary issuer

**Project relevance:** StubHub's AEG partnership makes it a relevant data context for secondary market pricing. Secondary market prices for Kings games — which reflect true willingness-to-pay — complement primary market data from SeatGeek in understanding full ticket demand curves.

---

## The NHL

**What it is:** The National Hockey League, the top professional ice hockey league in the world.

**Founded:** November 26, 1917 in Montreal, Quebec
**HQ:** New York City
**Commissioner:** Gary Bettman (since 1993)
**Teams:** 32 (25 US, 7 Canada)

**Key facts:**
- Regular season: 82 games per team, October through April
- Playoffs: 16 teams, 4 rounds, best-of-7 series; winner receives the Stanley Cup
- Stanley Cup is the oldest professional sports trophy in North America
- 5th-highest grossing professional sports league globally
- Reigning champions (as of 2025): Florida Panthers
- Major work stoppages: 1992 strike, 1994-95 lockout, 2004-05 (full season cancelled), 2012-13 lockout
- Current expansion teams include Seattle Kraken (2021) and Utah Mammoth (2024, relocated from Arizona)

**Project relevance:** The NHL schedule and team structure form the backbone of this project's data model. Game-level attributes — opponent, date, venue, home/away — drive the dimensional model. Understanding the league's structure (conferences, divisions, playoff seeding) is essential to building opponent quality metrics and rivalry flags in `dim_opponents`.
