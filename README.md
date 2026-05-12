# B2B Market & Channel Scanner

**Global market scan narrowed to U.S. account-level sell-through and channel expansion analysis.**

> This is a candidate portfolio simulation using public retailer pages, public market data, and manually collected screenshots. It does not use internal APR sales, margin, inventory, or buyer data.

---

## Project Overview

This project simulates the analytical workflow of a B2B global sales team evaluating market entry and channel expansion opportunities for a Korean beauty (K-beauty) company's portfolio.

The analysis began with a 9-country global scan across the U.S., Europe, and CIS, then narrowed to the U.S. as the core commercial priority based on import volume, purchasing power, regulatory readiness, and existing public channel presence. European and CIS retailer research is retained as cross-market reference intelligence.

**Individual project** — all research, analysis, and code by Changyeol (Aiden) Oh.

| Attribute | Detail |
|---|---|
| Scope | 9 countries, 18 retailers, 11 account briefs |
| U.S. Channels | Amazon, TikTok Shop, Ulta, Target |
| European Benchmark | Douglas, Boots, DM, Rossmann, Notino, Sephora France, Primor |
| CIS Reference | Kaspi.kz, Gold Apple (qualitative appendix) |
| Data Sources | UN Comtrade (HS 3304), World Bank, Google Trends, 18 public retailer websites, TikTok Shop public store data |
| Output | Streamlit dashboard (4 tabs) + PDF account brief generator |
| Deployment | [Streamlit Cloud](https://market-channel-scanner-account-breif.streamlit.app/) |

---

## Why the U.S.?

The scoring model evaluated 9 countries across 4 scenarios (base, growth-focused, risk-controlled, channel-expansion). The U.S. did not rank first in entry-opportunity score because competition is already intense. However, it emerged as the core commercial priority in this portfolio for three reasons:

1. **Largest import volume** — $1.02B in HS 3304 cosmetics imports (2023), 10x larger than the next market.
2. **Existing public channel presence** — Medicube and Aprilskin listings observed across Amazon, Ulta, Target, and TikTok Shop.
3. **Clear account-growth tasks** — The U.S. is not a new-entry market. The task is sell-through growth, SKU productivity, and cross-channel pricing governance.

UAE ranked highest in entry-opportunity signals but is treated as an expansion watchlist rather than the focus market, because this project targets the U.S. applicant region and prioritizes existing account-growth tasks.

---

## Pipeline

```
Stage 1: Global Market Scan
  Comtrade HS 3304 (1,721 rows)
  World Bank (77 rows)                    ──→  9-country scoring
  Google Trends (K-beauty + Medicube)          4-scenario sensitivity
  Expert assessment (regulation, competition)

Stage 2: Retailer Validation (18 channels)
  U.S.: Amazon, Ulta, Target, TikTok Shop, Soko Glam
  Europe: Douglas, Boots, DM, Rossmann,       ──→  competition_inv
          Notino, Sephora FR, Primor, Druni        calibration
  CIS: Kaspi.kz, Gold Apple, Allegro              market_role update
  Ukraine: EVA.UA (qualitative appendix)

Stage 3: U.S. Channel Strategy
  SKU × Channel Fit matrix                ──→  Account briefs
  Cross-channel pricing analysis               Priority ladder
  Aprilskin TikTok growth gap analysis         PDF generator

Stage 4: Dashboard & Deployment
  Streamlit 4-tab dashboard              ──→  Streamlit Cloud
  PDF account brief generator
```

---

## Key Findings

### Stage 1 → Stage 2: Manual research changed the model

The most significant outcome of this project is that retailer-level manual research revised initial scoring assumptions. Five of 9 countries had their competition scores adjusted after direct channel validation:

| Country | Stage 1 comp_inv | Stage 2 comp_inv | What changed |
|---|---|---|---|
| UK | 60 | 30 | Boots: 486 products, 35+ brands, Medicube 13 SKUs already listed |
| Germany | 65 | 40 | Douglas 715 + DM 82 + Rossmann 93, ISANA PB Korean Skincare discovered |
| France | 65 | 55 | Sephora FR: 264 products, Medicube 19 SKUs, editorial gap identified |
| Spain | 75 | 50 | Primor: 1,031 products, Medicube 13 SKUs all "Not Available" |
| Kazakhstan | 85 | 55 | Kaspi.kz: 28,213 listings, Medicube 407 listings with reviews |

### U.S. Channel Priority Ladder

Priority is based on near-term U.S. growth leverage, not channel prestige.

| Priority | Channel | Role | Key Signal |
|---|---|---|---|
| 1 | Amazon | Proof channel | 487 results, 121K+ public ratings on Zero Pore Pad |
| 2 | TikTok Shop | Growth acceleration | 5.7M+ shop-level public sold count, Aprilskin gap |
| 3 | Ulta | Brand elevation | 1,338 K-beauty products, Featured Brand placement |
| 4 | Target | Mass accessibility | 558 K-beauty products, post-Ulta Beauty Studio transition |
| 5 | Costco | Exploratory | 86 Korean skincare results, no Medicube observed |

### Cross-Channel Pricing Risk

TikTok Shop's frequent aggressive discounting creates channel conflict risk. Zero Pore Pad was observed at approximately $15 on Amazon, $21 at Ulta, and $20.90 on TikTok Shop (with deeper discounts in bundles). The recommended mitigation is format-based differentiation: TikTok-exclusive bundles not available at retail.

### Aprilskin TikTok Growth Gap

Medicube showed 5.7M+ shop-level public sold count vs Aprilskin's 53.5K on TikTok Shop — a large public traction gap suggesting room to test whether Medicube's observed content strategy can be adapted to Aprilskin.

---

## Dashboard Structure

| Tab | Purpose |
|---|---|
| Stage 1: Global Scan | 9-country scoring with 4-scenario sensitivity analysis. Explains why U.S. was selected. |
| Stage 2: U.S. Channel Map | U.S. channel overview, priority ladder, cross-channel pricing risk, account briefs |
| Stage 2: SKU x Channel Fit | Product-channel matrix showing which products fit which channels by price and format |
| Stage 2: Account Brief | PDF brief generator for buyer meeting preparation |

---

## Evidence Levels

This project distinguishes three evidence levels:

| Level | Meaning | Example |
|---|---|---|
| Observed | Directly seen from public retailer pages | Medicube 13 SKUs on Boots.com |
| Inferred | Interpretation based on observed signals | "Editorial gap" at Sephora France |
| Proposed | Sales hypothesis for buyer conversation | "AGE-R device in-store demo pilot" |

Account-level evidence status:

| Status | Meaning | Accounts |
|---|---|---|
| Public-source validated | Product listings directly confirmed | Amazon, Ulta, Boots, Douglas, DM, Rossmann, Primor |
| Public metrics observed | Public traction data (sold count, followers) confirmed | TikTok Shop |
| Representative storefront validation | Validated through one country storefront | Notino (via Notino.de) |
| France storefront validation | Validated through France storefront | Sephora France |
| Category presence observed | Category/filter presence confirmed, SKU detail pending | Target |
| Exploratory hypothesis | Limited direct evidence | Costco |

---

## Data Sources and Limitations

| Source | Usage | Limitation |
|---|---|---|
| UN Comtrade | Import volume/growth (HS 3304) | Preview mode (500 records/call). 2023 latest. |
| World Bank | GDP per capita, internet penetration | PPP-adjusted. 2023 latest. |
| Google Trends | K-beauty Topic + Medicube Search term | Relative indices only, not absolute volume. Separate normalizations. |
| Retailer websites | K-beauty category, brand filters, product counts, pricing | Point-in-time snapshots (May 2026). Not sell-through data. |
| TikTok Shop | Public sold counts, follower counts, video counts | Shop-level aggregates. May include seller duplication on marketplaces. |

**Google Trends caveat**: K-beauty Topic and Medicube Search term use separate normalizations. Cross-metric comparison (e.g., "Medicube is more popular than K-beauty in country X") is not valid. Both are used as directional signals only.

**Marketplace caveat**: Kaspi.kz (28,213 listings) and Allegro (543 offers) are marketplace platforms where the same product can appear from multiple sellers. Estimated unique product count for Kaspi is approximately 3,500-4,000 after ~7x seller duplication adjustment.

**Competition scores**: The `competition_inv` values are provisional expert assessments calibrated by retailer-level manual research. They are not derived from a statistical model.

---

## Russia / Ukraine: Qualitative Appendix

Russia and Ukraine are excluded from the comparable opportunity score — not because of weak demand, but because entry-feasibility risks are outside the model's current feature structure.

| Country | K-beauty Signal | Exclusion Reason |
|---|---|---|
| Russia | Gold Apple: 1,741 products, 200+ brands, Medicube 16 SKUs | Sanctions, payment, logistics, partner due-diligence risks |
| Ukraine | EVA.UA: 10,009 Korean cosmetics products | War-related infrastructure, logistics, recovery conditions |

---

## Reproducibility

```bash
# Clone
git clone https://github.com/ChangyeolAidenOh/market-channel-scanner.git
cd market-channel-scanner

# Install
pip install -r requirements.txt

# Run scoring (requires .env with COMTRADE_API_KEY)
python analysis/market_scoring.py

# Generate PDF briefs
python outputs/sales_brief_generator.py

# Run dashboard
streamlit run app/app.py
```

**Environment**: Python 3.10+, macOS (M2).

**API keys**: Comtrade API key required in `.env` file for data collection. Processed data is included in `data/processed/` for dashboard use without API access.

---

## File Structure

```
market-channel-scanner/
  analysis/
    market_scoring.py          # Stage 1: 9-country scoring + sensitivity
  app/
    app.py                     # Streamlit main app (4 tabs)
    tab_market_scanner.py      # Tab 1: Global Scan
    tab_us_channel_map.py      # Tab 2: U.S. Channel Map
    tab_sku_channel_fit.py     # Tab 3: SKU x Channel Fit
    tab_sales_brief.py         # Tab 4: Account Brief generator
  data/
    processed/
      market_scores.csv        # Scoring output
      country_features.csv     # Feature matrix
    reference/
      buyers.json              # 11 account briefs
      country_qualitative.json # Country-level context
      apr_products.json        # Product reference
  outputs/
    sales_brief_generator.py   # PDF brief generator
  .streamlit/
    config.toml                # Light theme
  requirements.txt
  README.md
```

---
