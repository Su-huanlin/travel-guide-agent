---
name: travel-guide-handbook
description: >-
  Builds a reviewable multi-day travel handbook from trip constraints: Markdown
  route/daily/execution guides, UTF-8 CSV data for itinerary/hotels/meals/budget/
  waypoints/booking/contingencies, SVG maps, then Excel/HTML/PDF deliverables with
  verification. Use when the user asks for a travel guide, itinerary handbook,
  自驾攻略, photography trip plan, route PDF/Excel pack, or provides dates,
  destination, pace, hotel tier, and transport constraints for a multi-day trip.
---

# Travel Guide Handbook

Produce a **source-first travel handbook**: editable `content/` + `data/` + `maps/`, then generated `output/` (PDF / Excel / HTML). Prefer comfort + photography self-drive trips; adapt for other modes.

## When to use

- User gives dates, origin/destination, pace, hotel preference, must-see / must-avoid.
- User wants printable handbook + booking checklist + budget + GPS waypoints.
- User asks to revise mid-trip against **actual current location/date**.

## Non-negotiable principles

1. **Confirm constraints before writing a full route.** Do not invent must-visit spots the user rejected.
2. **Source of truth is files, not chat.** Chat proposes; files commit.
3. **Pace honesty:** flag days that are transfer-only vs photography days; never hide 8–9h drive days as “easy”.
4. **Source grades:** A official/gov/airline/police; B recent platform pages; C trip notes; X unverified. Prefer A for tickets/roads/drones.
5. **Realtime override:** if user reports current date/location, replan remaining days immediately; mark past days as historical.
6. **No stale terms:** after route changes, grep and remove cancelled destinations from content, CSV, maps, verify forbidden list.

## Intake (ask only what is missing)

Collect before Day-by-day drafting:

| Field | Examples |
|---|---|
| Dates | start–end, nights |
| Party | adults/kids, rooms |
| Origin / return | city, airport preferences |
| Style | photography, comfort, budget, hiking |
| Transport | fly+rent, one-way dropoff, train |
| Must include / exclude | explicit list |
| Hotel tier | chain mid/high; no dirty felt tents |
| Hard limits | max drive hours/day, no overnight in X |
| Devices | camera/drone → UOM/local rules |
| Budget attitude | secondary vs hard cap |

Use [intake-template.md](intake-template.md) if starting a new trip folder.

## Project scaffold

Create (or reuse) a trip folder:

```text
trip-root/
  README.md
  content/
    01-route-design.md      # boundaries, master table, transport logic
    02-daily-guide.md       # Day N: theme, timeline, lodging, photo, Plan B
    03-execution-guide.md   # gear, fuel, tickets, backup, budget summary
  data/                     # UTF-8 CSV (utf-8-sig OK)
    daily_itinerary.csv
    hotels.csv
    meals.csv
    attractions.csv
    waypoints.csv
    weather_risk.csv
    booking_checklist.csv
    contingencies.csv
    budget.csv
    sources.csv
    gear.csv
  maps/
    overview-route.svg
    site-flows.svg
  scripts/
    generate_maps.py
    generate_outputs.py
    verify_outputs.py
    build_all.ps1           # or build_all.sh
  output/                   # generated only
```

CSV schemas and build details: [reference-pipeline.md](reference-pipeline.md).

## Workflow checklist

Copy and track:

```text
Travel handbook progress:
- [ ] 1. Intake + constraint lock
- [ ] 2. Route design (master table + deletes)
- [ ] 3. Daily guides (timeline + Plan B)
- [ ] 4. CSV data pack
- [ ] 5. Maps
- [ ] 6. Execution guide + booking checklist
- [ ] 7. Build outputs
- [ ] 8. Verify + stale-term sweep
- [ ] 9. Hand off paths + open decisions
```

### 1. Constraint lock

Write `content/01-route-design.md` **设计边界** first: dates, party, transport, include/exclude, hotel tier, hard rules. Get user OK on the master overnight table before fleshing every day.

### 2. Route design

Master table columns: 日期 | 住宿 | 核心安排 | 交通性质 | 负荷.

Rules of thumb:

- One **theme** per day when possible.
- Split “gallery road + mountain pass highway” onto separate days if both are photography goals.
- Prefer flight/rail hops over 10h+ empty transfers when budget allows.
- One-way rental to match unidirectional routes.
- Document reservation portals and entry names exactly (wrong gate = wasted day).

### 3. Daily guides

Each day in `02-daily-guide.md`:

- 今日主题
- 时间轴（clock times）
- 住宿（首选/备选 + 核验项）
- 摄影（焦段/机位纪律）
- Plan B（weather, closure, fatigue）

Mark cancelled alternatives as **删除**, not soft suggestions.

### 4. CSV data pack

Keep content and CSV aligned. Minimum useful set:

- `daily_itinerary.csv` — one row/day
- `hotels.csv` — candidates by night
- `meals.csv` — breakfast/lunch/dinner cues
- `attractions.csv` — tickets/shuttles/hours
- `waypoints.csv` — map search names, not fake precise GPS when unknown
- `booking_checklist.csv` — priority + channel + verify points
- `contingencies.csv` — trigger → action → never-do
- `budget.csv` — 3 tiers; **row sums must equal 小计**
- `sources.csv` — graded citations
- `weather_risk.csv`, `gear.csv`

### 5. Maps

- Overview: sequence of stays + flight dashed segments.
- Site flows: complex nodes (park shuttles, lake loops, canyon days).
- Labels must match current overnight plan after any replan.

### 6. Execution + booking

`03-execution-guide.md`: fuel nodes, backup workflow, ticket lock order, budget bands.

Booking order default: flights → scarce park lodgings/tickets → one-way rental + plate → highway reservations → remaining hotels.

### 7. Build

Prefer a single entrypoint:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_all.ps1
```

Pipeline: maps → xlsx/html → headless Edge/Chrome HTML→PDF → verify.

If no browser PDF: still ship HTML + XLSX; note PDF gap.

### 8. Verify

`verify_outputs.py` must check:

- XLSX exists, valid OOXML, required sheets non-empty
- HTML contains key current places; **forbids cancelled places/phrases**
- PDF magic `%PDF-` and minimum size

After edits: grep trip folder for cancelled destination names.

### 9. Hand off

Tell user:

- Paths under `output/`
- Open booking items
- Assumptions still needing confirmation (flight times, reservation windows)

## Mid-trip replan protocol

When user says “I am still in X on date Y”:

1. Freeze past days as historical (do not pretend they happened as planned).
2. Rebuild **only remaining nights** to return date.
3. Prefer merging transfer+scenery on approach roads; keep the hardest scenic highway on its own morning if possible.
4. Update booking checklist to “今天立刻” for tonight’s hotel + tomorrow’s permits.
5. Rebuild and verify before claiming done.

## Interaction style

- Short status + concrete next actions when user is traveling now.
- Do not re-add deleted destinations “for completeness”.
- When user asks route A vs B: answer time vs scenery tradeoff in a small table; recommend one default for tonight’s goal.

## Reference

- Pipeline, CSV headers, script roles → [reference-pipeline.md](reference-pipeline.md)
- Blank intake → [intake-template.md](intake-template.md)
- Worked example (2026 North Xinjiang) → [examples.md](examples.md)
