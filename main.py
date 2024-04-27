import os
import json
from nicegui import ui, app

version = "v1.0.0"
pages = []
app.add_static_files('/static', 'static')

for dir in os.walk("data"):
    for file in dir[2]:
        if file.endswith(".json"):
            page = str(file).replace(".json", "")
            pages.append(page)

with ui.card().classes("absolute-center"):
    ui.query('body').style('background: url("static/bg1.png") 0px 0px')
    ui.badge(f"岚枳的歌单 | {version}", outline=False)
    for page in pages:
        _page = ""
        if page == "中":
            _page = "zh"
        if page == "日":
            _page = "jp"
        if page == "英":
            _page = "en"
        ui.button(page, on_click=lambda _page = _page : ui.open(_page)).classes("w-full")
        @ui.page(f"/{_page}")
        def page_view(page = page):
            ui.query('body').style('background: url("static/bg.png") 0px 0px')
            file = f"data/{page}.json"
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            ui.badge(f"岚枳的歌单 | {page} | {version}", outline=False)
            for text in data:
                ui.chat_message(text, avatar='static/YoNi.jpg').props('bg-color="green-1"')

ui.run(title="岚枳的歌单", favicon="static/icon.png", host="0.0.0.0", port=11455, language="zh-CN", show=False, storage_secret='c2b95787b44c084fc7c7d2c8422917913e0b1a673892f7d1f644bcf73c133410')
