根据已有 content 文件，生成下列 CSV 的完整内容。每个文件用独立代码块，语言标签为 csv，并在代码块前用一行标记文件名，例如：

### data/daily_itinerary.csv
```csv
表头...
行...
```

需要生成：
1. data/daily_itinerary.csv
2. data/hotels.csv
3. data/meals.csv
4. data/attractions.csv
5. data/waypoints.csv
6. data/weather_risk.csv
7. data/booking_checklist.csv
8. data/contingencies.csv
9. data/budget.csv（含三档；最后含 小计 / 应急金10% / 预计总计；小计必须等于各项之和）
10. data/sources.csv
11. data/gear.csv

表头必须与模板一致。CSV 内字段如含逗号，用双引号包裹。
