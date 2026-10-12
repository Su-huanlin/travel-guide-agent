# Pipeline & data reference

## Directory contracts

| Path | Role | Edited by |
|---|---|---|
| `content/*.md` | Handbook prose | Agent + user |
| `data/*.csv` | Structured sheets | Agent + user |
| `maps/*.svg` | Printable vectors | `generate_maps.py` or hand edit |
| `scripts/*` | Build/verify | Agent maintains per trip |
| `output/*` | Deliverables | Generated only; do not hand-edit |

## Recommended CSV headers

### daily_itinerary.csv

```text
天数,日期,住宿地,主题,交通方式,纯驾驶/飞行,景区换乘与排队,门到门预计,建议出发,建议结束,主要流程,摄影重点,风险等级,Plan B
```

### hotels.csv

```text
日期/区域,酒店,档位,建议预算/晚,推荐理由,停车/接驳,摄影便利,关键核验项,参考链接
```

### meals.csv

```text
日期,区域,餐次,建议时间,场所类型,推荐内容,预算,执行提示,备注
```

### attractions.csv

```text
景点,日期,进入方式,离开方式,动线,建议用时,费用口径,核验要点,无人机注意,来源URL
```

### waypoints.csv

```text
区域,高德/地图搜索名,纬度参考,经度参考,点位类型,最佳时间,建议焦段,停车/抵达,精度与注意
```

Use map POI names; leave lat/lon blank when uncertain. Never invent precise GPS.

### booking_checklist.csv

```text
优先级,项目,建议完成时间,渠道,状态,核验要点
```

### contingencies.csv

```text
触发场景,判断条件,立即动作,替代安排,不可做
```

### budget.csv

```text
费用项目,性价比版/元,舒适版/元,摄影住宿优先版/元,计算假设,备注
```

Last three rows pattern:

```text
小计,...
应急金10%,...
预计总计2人,...
```

Validate: sum of item rows == 小计 for each tier.

### sources.csv

```text
等级,类别,来源标题,URL,用于本手册的信息,核验时间/备注
```

### weather_risk.csv

```text
日期,路段/景区,主要风险,执行策略,升级条件,信息源
```

### gear.csv

```text
类别,物品,数量,用途,备注
```

## Content outline

### 01-route-design.md

1. 设计边界  
2. 为什么不选常见错误路线  
3. 最终主线表  
4. 租车/航班逻辑  
5. 收尾原则 / 信息可信等级  

### 02-daily-guide.md

One `## Day N｜日期｜标题` section per day with theme, timeline, lodging, photo, Plan B.

### 03-execution-guide.md

Gear, daily backup, lenses, fuel nodes, ticket lock list, budget bands, source policy.

## Script roles

| Script | Responsibility |
|---|---|
| `generate_maps.py` | Write `maps/*.svg` from waypoints/route constants |
| `generate_outputs.py` | CSV→XLSX; MD+SVG→HTML handbook + A3 map HTML |
| `verify_outputs.py` | Size/sheet/term/PDF checks; maintain forbidden stale phrases |
| `build_all.ps1` / `.sh` | maps → outputs → headless print PDF → verify |

### HTML→PDF

Use Edge/Chrome headless:

```text
--headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=<out> <file-uri>
```

Copy HTML to a temp dir if file:// quirks appear; wait until PDF ≥ ~10KB.

### verify_outputs.py pattern

- XLSX: exists, zip OOXML, required sheet names, max_row ≥ 2  
- HTML: required current terms present; forbidden cancelled terms absent  
- PDF: `%PDF-` header; size floor (~50KB)

Update forbidden list whenever the user deletes a destination.

## Revision scripts

For large mid-trip rewrites, a one-shot `scripts/update_*.py` that rewrites Day N–end + CSV rows is OK. Prefer idempotent replacements and print which files changed. Still run full build + verify after.

## Encoding

- CSV/MD: UTF-8 (BOM `utf-8-sig` OK for Excel)  
- PowerShell console may garble Chinese; judge success by exit code + file mtime, not console glyphs  
- Keep `build_all.ps1` messages ASCII-safe if the shell code page is broken  

## Minimal viable deliverables

If time is short, ship in this order:

1. `01-route-design.md` master table  
2. `daily_itinerary.csv` + `booking_checklist.csv`  
3. `02-daily-guide.md`  
4. Full CSV + build  

Never claim PDF/Excel ready without running verify.
