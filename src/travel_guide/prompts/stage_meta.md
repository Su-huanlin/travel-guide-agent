根据旅行 brief，输出一个 JSON 对象（用 ```json 代码块），字段：

- title: 手册标题
- subtitle: 副标题
- cover_facts: 字符串数组，3–6 条封面要点（日期、人数、风格等）
- footer_note: 页脚提醒
- xlsx_itinerary / xlsx_waypoints / html_handbook / html_map / pdf_handbook / pdf_map: 合适的中文文件名
- required_terms: 校验时 HTML 必须出现的关键词（含核心目的地）
- forbidden_terms: 用户明确排除的地点/错误方案关键词

只输出 JSON 代码块。
