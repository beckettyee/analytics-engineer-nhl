# Dynamic Pricing Insights

## What Is Dynamic Pricing?

Dynamic pricing — also called demand pricing, surge pricing, or time-based pricing — is a revenue management strategy in which prices are set flexibly based on current market demand rather than at a fixed rate. The core principle is simple: when more people want something than there is supply, the price goes up; when demand is weak, the price drops to stimulate purchases.

Dynamic pricing is common in airlines, hotels, rideshare (Uber surge pricing), and e-commerce. It entered mainstream sports and live entertainment in the 2010s.

## Origins in Sports

The San Francisco Giants pioneered dynamic pricing in professional sports, partnering with startup Qcue to pilot flexible pricing on approximately 2,000 seats in their early experiments before expanding to their full venue around 2010. The goal was to capture the price premium for high-demand matchups (rival teams, weekend games, playoff races) that the secondary market was already capturing via ticket resale.

Baseball's success with dynamic pricing prompted rapid adoption across other sports:
- **MLB** teams broadly adopted dynamic pricing through the early 2010s
- **NBA** and **NHL** teams followed, applying the same demand variables to their shorter regular seasons
- **NCAA** athletic departments began experimenting with dynamic pricing for marquee football and basketball matchups

## How Dynamic Pricing Works in Sports

Sports ticket dynamic pricing models typically incorporate the following demand signals:

| Factor | Effect on Price |
|--------|----------------|
| **Opponent quality** | High-profile or rival opponents drive up demand (and price) |
| **Day of week** | Weekend games command a premium over weekday games |
| **Game timing** | Holiday games, rivalry week, playoff-race games price higher |
| **Team performance** | Teams on winning streaks or in playoff contention see higher demand |
| **Weather** (outdoor venues) | Favorable weather increases demand for open-air events |
| **Seat location** | Premium zones (lower bowl, club level) priced dynamically relative to baseline |
| **Days until event** | Prices often rise as the event approaches if inventory is tight |

The typical implementation uses algorithms that monitor current sales velocity, remaining inventory, and comparable historical events to set prices in near-real-time. Teams update prices daily or more frequently during peak demand windows.

## Ticketmaster and the 2022 Controversy

Ticketmaster introduced dynamic pricing across its platform in 2022, bringing the practice to mainstream consumer attention in a highly visible and controversial way:

- **Blink-182 reunion tour** tickets were listed for over $600 through dynamic pricing
- **Bruce Springsteen** tickets reached $4,000-$5,000 for premium seats
- **Oasis Live '25 Tour** presale triggered massive backlash in the UK when prices surged during high-traffic on-sale periods

These incidents intensified calls for regulation of ticketing practices and contributed to the DOJ's May 2024 antitrust suit against Live Nation Entertainment. A jury found Live Nation guilty of maintaining an illegal monopoly in April 2026.

The controversy highlighted a key tension in dynamic pricing: while it is economically rational (prices reflect actual willingness-to-pay), it can feel exploitative to fans who have budgeted based on advertised face values, and it transfers secondary market profits from resellers to the original ticket issuer.

## SeatGeek's Approach: Smart Pricing

SeatGeek launched its AI-powered "Smart Pricing" tool for resellers in February 2024. This tool helps individual resellers on SeatGeek's marketplace set competitive prices based on:
- Current comparable listings on the platform
- Historical sales data for similar events
- Demand signals (event popularity, days until event, remaining inventory)

SeatGeek's DealScore algorithm rates seats on a 1-100 scale to help buyers identify fair value, effectively creating a two-sided dynamic pricing market. SeatGeek also complies with FTC all-in pricing guidelines, displaying fees upfront — a differentiator from Ticketmaster and StubHub, both of which have faced criticism and legal action over drip pricing practices.

## NHL-Specific Dynamics

In the NHL context, the most significant demand drivers for ticket pricing include:

**Opponent rivalries:** Games against division rivals generate the highest organic demand. For the LA Kings, division rivals within the Pacific Division (Vegas Golden Knights, Edmonton Oilers, Calgary Flames, Vancouver Canucks) tend to drive elevated secondary market prices. The Kings-Oilers rivalry has been particularly intense given their four consecutive playoff series from 2022-2025.

**Playoff implications:** Late-season games with playoff seeding implications see spikes in demand that dynamic pricing systems should capture.

**Star power:** When marquee players visit (Connor McDavid, Nathan MacKinnon, Sidney Crosby), demand rises measurably for Kings home games — this is directly observable in SeatGeek listing data.

**Day-of-week and back-to-backs:** Saturday and Sunday games consistently outperform Tuesday/Wednesday games on attendance and ticket prices. Back-to-back games (Kings playing on consecutive nights) can suppress demand for the second game.

**Season trajectory:** Teams performing above expectations (hot streaks, first-place standings) see sustained demand increases. The inverse is also true — struggling teams see secondary market prices collapse.

## Industry Trends

Several macro trends are shaping sports ticket pricing:

1. **Convergence of primary and secondary markets:** SeatGeek's entry into primary ticketing (and Ticketmaster's dynamic pricing) is blurring the line between face-value and resale pricing. Teams increasingly set initial prices dynamically rather than fixing them at season start.

2. **All-in pricing transparency:** FTC pressure is pushing platforms toward displaying total prices (including fees) upfront. SeatGeek already does this; Ticketmaster and StubHub are being pushed to follow.

3. **Antitrust and regulatory risk:** Live Nation Entertainment's April 2026 illegal monopoly verdict introduces uncertainty about Ticketmaster's role in venue contracts. This could accelerate opportunities for competitors like SeatGeek and AXS (AEG's own ticketing platform).

4. **AI and machine learning:** Pricing algorithms are becoming more sophisticated, incorporating sentiment data, social media signals, and real-time inventory across competing platforms.

5. **FIFA World Cup 2026:** FIFA announced dynamic pricing for the 2026 World Cup (hosted in the US, Canada, and Mexico), signaling mainstream acceptance at the highest levels of international sport.

## Connection to This Project

This project models the relationship between game attributes and ticket demand for LA Kings games using SeatGeek API data. The core analytical question — "which games command the highest ticket prices and why?" — is precisely the question that dynamic pricing algorithms must answer.

By building `dim_opponents` (with opponent quality scores and rivalry flags), `dim_dates` (with weekend/holiday flags), and `fact_games` (with SeatGeek min/avg/max pricing per game), this project creates the dimensional foundation that would feed a Kings dynamic pricing model. The Streamlit dashboard surfaces these insights for a non-technical audience, allowing a pricing or revenue management team to see which upcoming games represent high-demand opportunities.

The analysis demonstrates the kind of data modeling and analytical thinking that an Analytics Engineer at AEG would apply to real Kings pricing decisions.
