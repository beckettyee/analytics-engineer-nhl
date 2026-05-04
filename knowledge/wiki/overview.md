# Overview: LA Kings, AEG, and the NHL Ticketing Landscape

## The LA Kings

The Los Angeles Kings are a National Hockey League franchise founded on June 5, 1967, by Jack Kent Cooke. Based in Downtown Los Angeles, they compete in the Western Conference Pacific Division and play their home games at Crypto.com Arena. The Kings are one of the most storied franchises in the NHL's Sun Belt expansion, having won two Stanley Cup championships — in 2012 (defeating the New Jersey Devils) and 2014 (defeating the New York Rangers).

The 1988 trade that brought Wayne Gretzky from the Edmonton Oilers to Los Angeles is widely credited with legitimizing hockey on the West Coast and growing the sport's national profile. The franchise has produced several Hall of Fame-caliber players including Anze Kopitar (who announced his retirement in September 2025 after 20 seasons), Drew Doughty, Jonathan Quick (who retired April 13, 2026), and Dustin Brown.

The 2025-26 season marked a difficult transition. After four consecutive first-round playoff exits to the Edmonton Oilers (2022-2025), the Kings parted ways with head coach Jim Hiller on March 1, 2026, replacing him with interim coach D.J. Smith. Under new general manager Ken Holland, the Kings made the playoffs as a wild card but were eliminated by the Presidents' Trophy-winning Colorado Avalanche 4-1 in the first round.

## AEG and Crypto.com Arena

The Kings are owned by AEG (Anschutz Entertainment Group), founded in 1994 by billionaire Philip Anschutz. AEG is the world's largest owner of sports teams and venues and the second-largest live entertainment presenter globally (after Live Nation). The company hosts more than 100 million guests annually across 13,000+ live events at 100+ venues worldwide. Its sports portfolio includes the LA Kings, LA Galaxy, Ontario Reign, and Eisbären Berlin.

Crypto.com Arena — home of the Kings since the 1999-2000 season — opened on October 17, 1999 as Staples Center. It was renamed on December 25, 2021 in a deal with Crypto.com valued at $700 million over 20 years, which at the time was the most valuable naming rights contract in sports history. The arena seats 18,145 for hockey and 19,079 for basketball. It also hosts the NBA's Los Angeles Lakers and WNBA's Los Angeles Sparks. The venue has 160 luxury suites and 2,500 club seats, and has hosted the Grammy Awards 23 times. It will serve as an Olympic venue during the 2028 Los Angeles Games.

AEG's influence on the ticketing industry is significant. As a major venue operator and team owner, AEG sits at the intersection of primary and secondary ticketing markets. When the Department of Justice approved the Ticketmaster-Live Nation merger in 2010, it required Live Nation to license its ticketing software to AEG — acknowledging AEG's role as a major competing force. AEG has also partnered with StubHub, which serves as an official resale marketplace for AEG venues.

## The NHL Ticketing Landscape

The NHL was founded on November 26, 1917, in Montreal. The league now comprises 32 teams — 25 in the United States and 7 in Canada — playing an 82-game regular season from October through April, followed by a 16-team playoff bracket competing for the Stanley Cup. The NHL is the fifth-highest grossing professional sports league globally, with commissioner Gary Bettman leading the organization since 1993.

NHL ticket pricing operates in a complex ecosystem dominated by a few major players:

- **Ticketmaster** (a subsidiary of Live Nation Entertainment, $23.16B revenue in 2024) controls primary ticketing for most NHL venues. It introduced dynamic pricing across its platform in 2022 and has faced mounting regulatory scrutiny — a DOJ antitrust suit filed in May 2024, with a jury finding an illegal monopoly in April 2026.

- **SeatGeek** is an emerging challenger in primary and secondary ticketing, known for its DealScore seat valuation algorithm and AI-powered Smart Pricing tool (launched February 2024). SeatGeek holds NHL primary ticketing contracts with the Florida Panthers and Utah Mammoth, and became the official MLB marketplace in 2023.

- **StubHub** (owned by Viagogo/StubHub Holdings since 2020, $1.77B revenue in 2024, IPO September 2025) is the dominant secondary market platform and has an official resale partnership with AEG venues.

Dynamic pricing — adjusting ticket prices in real time based on demand, opponent quality, day of week, and team performance — has become standard practice across major sports leagues. The SF Giants pioneered dynamic pricing in baseball starting around 2010, and the NHL, NBA, and NCAA quickly adopted similar approaches.

## How This Project Connects These Domains

This project builds an NHL Opponent and Schedule Intelligence Tool that uses SeatGeek API data to analyze ticket pricing patterns for Kings games. By pulling SeatGeek event listings across the NHL, it models how opponent quality, schedule position (back-to-backs, weekends), team performance, and rivalry status drive ticket demand and pricing.

The analysis is directly relevant to AEG's business as a team owner and venue operator making real-time pricing decisions. Understanding the relationship between game attributes (who is the opponent, when is the game, how is the team performing) and ticket market demand is core to the dynamic pricing strategies that modern sports organizations use to maximize revenue without alienating fans. This project demonstrates those analytics capabilities using the actual data sources and dimensional modeling patterns an analytics engineer at AEG would work with.
